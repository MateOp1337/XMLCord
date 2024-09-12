## XMLCord Documentation | Arguments

### Argument Requirements

1. **Exact Names**: Argument names must exactly match those specified in the Discord.py documentation. Ensure that the names used are correct and consistent with the expected values.

2. **Correct Types**: Arguments must be of the correct type:
   - `str`, `text`, or `string` for strings.
   - `int`, `number`, or `integer` for integers.
   - `list` or `array` for lists (elements separated by spaces).
   - `dict` or `json` for JSON objects.

3. **Valid Values**: Ensure that the argument values conform to the expected format and range for their type.

4. **Required vs. Optional**: Clearly specify which arguments are required and which are optional. If an argument is optional, provide a default value if possible.

5. **Documentation Consistency**: Cross-reference the argument names and types with the latest Discord.py documentation to ensure accuracy.

### Argument Conversion

- **String to Boolean**: `true` and `false` values are converted to `True` and `False`.
- **String to Integer**: Values are converted to integers if specified as `int`, `number`, or `integer`.
- **String to List**: Comma-separated values or space-separated values are converted to lists.
- **String to Dictionary**: JSON-formatted strings are parsed into dictionaries.

### Example Usage

```xml
<command>
  <argument name='user' type='str'/>
  <argument name='age' type='int'/>
  <argument name='roles' type='list'/>
</command>
```

In the example above:
- `user` is expected to be a string.
- `age` should be an integer.
- `roles` will be parsed as a list of strings.

### Error Handling

- If an argument's type does not match the expected type, a `ValueError` will be raised.
- Ensure all required arguments are provided, otherwise, a `ValueError` will be raised indicating the missing argument.

