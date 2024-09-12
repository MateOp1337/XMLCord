## XMLCord Documentation | Views (Buttons and select menus)

### 1. View Components

1. **Buttons**: Interactive elements that users can click. Buttons can have different styles and can trigger actions when clicked.

2. **Select Menus**: Dropdown menus that allow users to select an option from a list. Select menus can have multiple options and support single or multiple selections.

### 2. Creating Views

**Buttons**:
- **Attributes**:
  - `label`: The text displayed on the button.
  - `style`: The style of the button (`primary`, `secondary`, `success`, `danger`).
  - `disabled`: Whether the button is disabled (`true` or `false`).
  - `url`: Optional URL that the button links to.

**Select Menus**:
- **Attributes**:
  - `placeholder`: The placeholder text displayed when no option is selected.
  - `min_values`: The minimum number of values that can be selected.
  - `max_values`: The maximum number of values that can be selected.
  - `options`: List of options in the select menu.

### 3. Example XML Configuration

```xml
<views>
    <my_view>
        <button>
            <label>Press me!</label>
            <style>blue</style>
            <on_click>
                <response type='message'>
                    <content>Hi!</content>
                    <ephemeral>true</ephemeral>
                </response>
            </on_click>
        </button>
        <button disabled='true'>
            <label>Don't press me!</label>
            <style>green</style>
            <on_click>
                <response type='message'>
                    <content>Hi!</content>
                    <ephemeral>true</ephemeral>
                </response>
            </on_click>
        </button>
        <select_menu>
            <option value='option1'>
                <label>Option 1</label>
                <description>This is first option</description>
                <on_select>
                    <response type='message'>
                        <content>This is a first option. Hi!</content>
                        <ephemeral>true</ephemeral>
                    </response>
                </on_select>
            </option>
            <option value='option2'>
                <label>Option 2</label>
                <description>This is second option</description>
                <on_select>
                    <response type='message'>
                        <content>This is a second option. Hello!</content>
                        <ephemeral>true</ephemeral>
                    </response>
                </on_select>
            </option>
        </select_menu>
    </my_view>
</views>
```
