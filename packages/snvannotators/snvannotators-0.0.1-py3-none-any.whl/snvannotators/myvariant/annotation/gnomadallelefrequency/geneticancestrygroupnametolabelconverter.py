"""Convert computer-friendly genetic ancestry group name to human-readable label."""


class GeneticAncestryGroupNameToLabelConverter:
    """Convert computer-friendly genetic ancestry group name to human-readable label."""

    GROUP_NAME_LOOKUP = {
        "afr": "African/African American",
        "amr": "Admixed American",
        "asj": "Ashkenazi Jewish",
        "eas": "East Asian",
        "fin": "European Finnish",
        "nfe": "Non-Finnish European",
        "oth": "Other",
        "sas": "South Asian",
        "male": "XY",
        "female": "XX",
        "jpn": "Japanese",
        "kor": "Korean",
        "oea": "Other East Asian",
        "bgr": "Bulgarian",
        "est": "Estonian",
        "nwe": "North-western European",
        "onf": "Other non-Finnish European",
        "seu": "Southern European",
        "swe": "Swedish",
    }

    def __init__(self, name: str, sep: str = ", "):
        self.name = name
        self.sep = sep

    def convert(self) -> str:
        """Convert

        Returns:
            str: human-friendly label.
        """
        groups = self.name.split("_")
        label_parts = []
        for group in groups[1:]:
            label = GeneticAncestryGroupNameToLabelConverter.GROUP_NAME_LOOKUP.get(
                group, None
            )
            if label is not None and label:
                label_parts.append(label)
        return self.sep.join(label_parts)
