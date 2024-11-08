from typing import List
from .choice_code import ChoiceCode, ChoiceCodeSet
from .display_format import DisplayFormat
from .exceptions import InvalidChoiceCodeError, InvalidChoicesResponseError


class Choice:
    def __init__(self, code: ChoiceCode, description: str) -> None:
        self.code = code
        self.description = description


class ChoiceSection:
    def __init__(self, introduction: str, manager: "ChoiceManager") -> None:
        """
        Initialize a section of related choices with an introduction text.

        A ChoiceSection represents a group of related choices that are presented together,
        managed by a ChoiceManager. The section starts with no choices - they must be
        added using add_choice().

        Args:
            introduction (str): The text that introduces and explains this section of choices.
                Write this as though for a human who is filling out a questionnaire. For example,
                you may say something like "Choose up to three of the following options that best ..."
            manager (ChoiceManager): The ChoiceManager instance that manages this section
        """
        self.introduction = introduction
        self.manager = manager
        self.choices: List[Choice] = []

    def add_choice(self, description: str) -> ChoiceCode:
        """
        Adds a choice to the section.

        Args:
            description (str): The description of the choice.

        Returns:
            ChoiceCode: The code assigned to the new choice.

        Raises:
            ValueError: If the description is empty.
        """
        if not description.strip():
            raise ValueError("Choice description cannot be empty.")
        code = self.manager.get_next_choice_code()
        choice = Choice(code, description)
        self.choices.append(choice)
        return code

    def display(self, format: DisplayFormat) -> str:
        """
        Displays the section in the specified format.

        Args:
            format (DisplayFormat): The format to display the section in.

        Returns:
            str: The formatted display of the section.

        Raises:
            NotImplementedError: If the specified format is not supported.
        """
        if format == DisplayFormat.MARKDOWN:
            markdown_output = f"### {self.introduction}\n\n"
            for choice in self.choices:
                markdown_output += f"- **{choice.code.code}**: {choice.description}\n"
            return markdown_output
        else:
            raise NotImplementedError(
                f"Display format '{format.value}' is not supported."
            )


class ChoiceManager:
    """Manages sections and choices for the multiple-choice questionnaire."""

    def __init__(self) -> None:
        self.sections: List[ChoiceSection] = []
        self.next_choice_code = 1

    def add_section(self, introduction: str) -> ChoiceSection:
        """
        Adds a new section to the questionnaire.

        Args:
            introduction (str): The text that introduces and explains this section of choices.
                Write this as though for a human who is filling out a questionnaire. For example,
                you may say something like "Choose up to three of the following options that best ..."

        Returns:
            ChoiceSection: The newly created section.
        """
        section = ChoiceSection(introduction, self)
        self.sections.append(section)
        return section

    def get_next_choice_code(self) -> ChoiceCode:
        """
        Generates the next available choice code.

        Returns:
            ChoiceCode: The next available choice code.
        """
        code = ChoiceCode(self.next_choice_code)
        self.next_choice_code += 1
        return code

    def is_valid_choice_code(self, code: ChoiceCode) -> bool:
        """
        Checks if a given choice code is valid.

        Args:
            code (ChoiceCode): The choice code to validate.

        Returns:
            bool: True if the code is valid, False otherwise.
        """
        return 1 <= code.code < self.next_choice_code

    def validate_choice_code(self, code: ChoiceCode) -> None:
        """
        Validates a choice code and raises an exception if it's invalid.

        Args:
            code (ChoiceCode): The choice code to validate.

        Raises:
            InvalidChoiceCodeError: If the choice code is invalid.
        """
        if not self.is_valid_choice_code(code):
            raise InvalidChoiceCodeError(f"Choice code {code.code} is invalid.")

    def prompt_for_choices(self, format: DisplayFormat, introduction: str) -> str:
        """
        Creates a prompt that displays the questionnaire and instructions the model how
        to respond with a list of choices. The prompt opens with a terse, vanilla instruction
        like "Make choices as instructed below."

        Args:
            format (DisplayFormat): The format to display the sections in.
            introduction (str): The text that introduces and explains the questionnaire.
                Write this as though for a human who will fill it out. For example,
                you may say something like "Analyze the situation in this chat by filling
                out the following questionnaire."

        Returns:
            str: The complete prompt including choices and response instructions.
        """
        opening = (
            "Make choices as instructed below. Reply with just a comma-separated "
            "list of the integer codes for your choices.\n"
        )
        choices = self.display(format)
        instructions = (
            "\nResponse Instructions:\n"
            "- Respond ONLY with the numbers of your chosen options.\n"
            "- Separate multiple choices with commas.\n"
            "- Example valid responses: '1' or '1,3' or '2,4,6' (without the quotes).\n"
            "- Do not include any other text or punctuation.\n"
        )
        return introduction + "\n" + opening + choices + instructions

    def display(self, format: DisplayFormat) -> str:
        """
        Displays all sections in the specified format.

        Args:
            format (DisplayFormat): The format to display the sections in.

        Returns:
            str: The formatted display of all sections.

        Raises:
            NotImplementedError: If the specified format is not supported.
        """
        if format == DisplayFormat.MARKDOWN:
            return "\n\n".join(section.display(format) for section in self.sections)
        else:
            raise NotImplementedError(
                f"Display format '{format.value}' is not supported."
            )

    def validate_choices_response(self, response: str) -> ChoiceCodeSet:
        """
        Validates a choices response string and returns a ChoiceCodeSet.

        Args:
            response (str): The response string containing comma-separated choice numbers.

        Returns:
            ChoiceCodeSet: A set containing the validated choice codes.

        Raises:
            InvalidChoicesResponseError: If any validation checks fail. The error message
                will contain a complete list of all validation problems found. It is intended
                to be fed back to the LLM if there is a retry.
        """
        errors = []
        choice_set = ChoiceCodeSet()

        # Check for empty response
        cleaned = response.strip()
        if not cleaned:
            errors.append("Response cannot be empty")
            raise InvalidChoicesResponseError("Response cannot be empty")

        # Parse and validate number format
        try:
            numbers = [int(num.strip()) for num in cleaned.split(",")]
        except ValueError:
            errors.append("Response must contain only numbers separated by commas")
            raise InvalidChoicesResponseError(errors[0])

        # Track seen numbers to detect duplicates
        seen_numbers = set()

        # Validate each number
        for num in numbers:
            # Check for duplicates
            if num in seen_numbers:
                errors.append(f"Choice {num} is duplicated")
            seen_numbers.add(num)

            # Validate choice code
            code = ChoiceCode(num)
            if not self.is_valid_choice_code(code):
                errors.append(f"Choice {num} is not a valid option")
                continue

        # If any errors occurred, raise with consolidated message
        if errors:
            error_msg = "\n".join([f"- {err}" for err in errors])
            raise InvalidChoicesResponseError(
                f"Invalid response. The following problems were found:\n{error_msg}"
            )

        # Only create the final set if all validation passed
        for num in numbers:
            choice_set.add(ChoiceCode(num))

        return choice_set
