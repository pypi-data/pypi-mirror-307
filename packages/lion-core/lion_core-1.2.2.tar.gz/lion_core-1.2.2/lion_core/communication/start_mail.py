from typing import Any

from typing_extensions import override

from lion_core.abc import Signal
from lion_core.generic import Element, Exchange
from lion_core.types import Field, LnID

from .mail import Mail
from .package import Package


class StartMail(Element, Signal):
    """A start mail node that triggers the initiation of a process."""

    mailbox: Exchange = Field(
        default_factory=Exchange, description="The pending start mail"
    )

    @override
    def trigger(
        self,
        context: Any,
        structure_id: LnID,
        executable_id: LnID,
    ) -> None:
        """Triggers the start mail by including it in the mailbox.

        Args:
            context: The context to be included in the start mail.
            structure_id: The ID of the structure to be initiated.
            executable_id: The ID of the executable to receive the start mail.
        """
        start_mail_content = {"context": context, "structure_id": structure_id}
        pack = Package(category="start", package=start_mail_content)
        start_mail = Mail(
            sender=self.ln_id,
            recipient=executable_id,
            package=pack,
        )
        self.mailbox.include(start_mail, "out")


# File: lion_core/communication/start_mail.py
