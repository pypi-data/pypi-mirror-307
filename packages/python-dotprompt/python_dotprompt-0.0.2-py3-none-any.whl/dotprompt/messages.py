import re
from typing import Any, List, Optional

from .types import DocumentData, MessageData, Part, MediaPart


class MessageProcessor:
    """Handles conversion between template strings and message structures"""

    ROLE_REGEX = re.compile(r"<<<dotprompt:(?:role:[a-z]+|history)>>>")
    PART_REGEX = re.compile(r"<<<dotprompt:(?:media:url|section).*?>>>")

    def to_messages(
        self,
        rendered_string: str,
        context: Optional[List[DocumentData]] = None,
        history: Optional[List[MessageData]] = None,
    ) -> List[MessageData]:
        """Convert rendered string to a list of messages"""
        current_message: MessageData = {"role": "user", "source": ""}
        message_sources: list[MessageData] = [current_message]

        last_end = 0
        for match in self.ROLE_REGEX.finditer(rendered_string):
            current_source = str(current_message["source"])
            # Add text before this marker
            if match.start() > last_end:
                current_message["source"] = (
                    str(current_message["source"])
                    + rendered_string[last_end : match.start()]
                )

            marker = match.group(0)
            if marker == "<<<dotprompt:history>>>":
                if str(current_message["source"]).strip():
                    message_sources.append({"role": "model", "source": ""})

                if history:
                    for hist_msg in history:
                        hist_metadata = hist_msg.get("metadata", {})
                        if isinstance(hist_metadata, dict):
                            message_sources.append(
                                {
                                    **hist_msg,
                                    "metadata": {
                                        **(hist_metadata),
                                        "purpose": "history",
                                    },
                                }
                            )
                current_message = {"role": "model", "source": ""}
                message_sources.append(current_message)
            else:  # Role change
                role = marker[len("<<<dotprompt:role:") : -3]  # Extract role name
                if str(current_message["source"]).strip():
                    current_message = {"role": role, "source": ""}
                    message_sources.append(current_message)
                else:
                    current_message["role"] = role

            last_end = match.end()

        # Add remaining text
        if last_end < len(rendered_string):
            current_message["source"] = (
                str(current_message["source"]) + rendered_string[last_end:]
            )

        # Convert to final messages, filtering empty ones
        messages = []
        for msg in message_sources:
            if msg.get("content") or str(msg.get("source", "")).strip():
                message: MessageData = {
                    "role": msg["role"],
                    "content": msg.get("content") or self.to_parts(str(msg["source"])),
                }
                if msg.get("metadata"):
                    message["metadata"] = msg["metadata"]
                messages.append(message)

        return messages

    def to_parts(self, source: str) -> List[Part]:
        """Convert source string to a list of parts"""
        parts: List[Part] = []
        last_end = 0
        preserve_next_whitespace = False

        for match in self.PART_REGEX.finditer(source):
            # Add text before this match if any
            if match.start() > last_end:
                text = source[last_end : match.start()]
                if text.strip():
                    if preserve_next_whitespace:
                        parts.append({"text": text})
                    else:
                        parts.append({"text": text.strip()})

            marker = match.group(0)

            if "media:url" in marker:
                # Parse media URL and optional content type
                components = marker[marker.index("url") + 4 : -3].strip().split()
                url = components[0]
                part: MediaPart = {"media": {"url": url}}
                if len(components) > 1:
                    part["media"]["contentType"] = components[1]
                parts.append(part)
                preserve_next_whitespace = True
            elif "section" in marker:
                # Parse section name
                section_name = marker[marker.index("section") + 7 : -3].strip()
                parts.append({"metadata": {"purpose": section_name, "pending": True}})
                preserve_next_whitespace = False

            last_end = match.end()

        # Add any remaining text
        if last_end < len(source):
            remaining_text = source[last_end:]
            if remaining_text.strip():
                if preserve_next_whitespace:
                    parts.append({"text": remaining_text})
                else:
                    parts.append({"text": remaining_text.strip()})

        return parts
