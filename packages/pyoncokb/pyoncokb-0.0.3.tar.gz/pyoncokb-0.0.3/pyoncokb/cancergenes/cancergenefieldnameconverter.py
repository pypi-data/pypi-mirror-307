"""Convert dict key from camel case to snake case."""


class CancerGeneFieldNameConverter:
    """Convert dict key from camel case to snake case."""

    @staticmethod
    def camel_to_snake_case(key: str) -> str:
        """Convert a single camel case string to snake case.

        :param key: a field name of CancerGene, an OncoKB API model.
        :type key: str
        :return: a new field name.
        :rtype: str
        """
        result = [key[0].lower()]
        for char in key[1:]:
            if char.isupper():
                result.extend(["_", char.lower()])
            else:
                result.append(char)
        return "".join(result)

    @staticmethod
    def convert(obj):
        """Recursively convert keys in a dictionary to snake case.

        :param obj: a dict or a list of dict for CancerGene, a OncoKB API model.
        :type obj: list or dict
        :return: a list if :param:`obj` is a dict, a dict if :param:`obj` is a dict.
        :rtype: list or dict
        """
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                if key == "grch37RefSeq":
                    new_key = "grch37_refseq"
                elif key == "grch38RefSeq":
                    new_key = "grch38_refseq"
                elif key == "mSKHeme":
                    new_key = "msk_heme"
                elif key == "mSKImpact":
                    new_key = "msk_impact"
                elif key == "sangerCGC":
                    new_key = "sanger_cgc"
                else:
                    new_key = CancerGeneFieldNameConverter.camel_to_snake_case(key)
                new_value = CancerGeneFieldNameConverter.convert(value)
                new_dict[new_key] = new_value
            return new_dict
        elif isinstance(obj, list):
            return [CancerGeneFieldNameConverter.convert(item) for item in obj]
        else:
            return obj
