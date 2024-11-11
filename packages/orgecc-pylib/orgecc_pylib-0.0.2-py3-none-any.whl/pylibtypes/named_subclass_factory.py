def create_named_subclass(base_class: type, instance_name: str, prefix: str = "") -> type:
    """
    Creates a named subclass of a given base class.

    Args:
        base_class: The class to inherit from
        instance_name: Name to convert into class name (e.g. 'my-name-1')
        prefix: Optional prefix for the class name

    Returns:
        A new subclass of base_class with formatted name

    Example:
        >>> MyClass = create_named_subclass(BaseClass, "my-name-1", "Custom")
        # Creates class CustomMyName1(BaseClass)
    """
    # Convert instance-name-1 to InstanceName1
    class_name_parts = instance_name.split('-')
    class_name = ''.join(part.capitalize() for part in class_name_parts)

    full_class_name = f"{prefix or base_class.__name__}{class_name}"

    return type(
        full_class_name,
        (base_class,),
        {
            '__doc__': f'{base_class.__name__} subclass for "{instance_name}"',
            '_instance_name': instance_name
        }
    )

# class AttributeFallbackProxy:
#     """
#     Delegates attribute access to a primary source, falling back to a secondary source
#     if the attribute is not found. Useful for combining prompt templates with default values.
#
#     Example:
#         base_prompts = CoderPrompts()
#         template_prompts = CoderPromptsTemplateName1()
#         adapter = AttributeFallbackProxy(primary=template_prompts, fallback=base_prompts)
#     """
#
#     def __init__(self, *, primary, fallback):
#         self._primary = primary
#         self._fallback = fallback
#
#     def __getattr__(self, name: str):
#         """
#         Attempts to get attribute from primary source first,
#         falls back to secondary source if not found.
#         """
#         try:
#             return getattr(self._primary, name)
#         except AttributeError:
#             return getattr(self._fallback, name)
#
#     def __dir__(self):
#         """
#         Returns combined set of attributes from both sources
#         for better IDE support and introspection.
#         """
#         return sorted(set(dir(self._primary)) | set(dir(self._fallback)))
