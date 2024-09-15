# XMLCord Documentation | Modals

*New in version a1.0.4*

### 1. Creating Modals

To create a modal, define it in the `<modals>` section of the bot's XML configuration. Example:

```xml
<modals>
  <example_modal title="Example Modal" timeout="None">
    <inputs>
      <input label="Your Input" placeholder="Enter something" type="short"/>
      <input label="Additional Info" type="paragraph"/>
    </inputs>
    <on_submit>
      <response type='message'>
        <content>Modal submitted with input: {inp(Your Input)}</content>
        <ephemeral>true</ephemeral>
      </response>
    </on_submit>
  </example_modal>
</modals>
```

### 2. Available Modal Attributes

Here are the attributes you can use for modals in XMLCord:

- **name**: The name of the modal (e.g., `name='example_modal'`).
- **title**: The title displayed at the top of the modal (e.g., `title='Example Modal'`).
- **timeout**: The timeout for the modal in seconds (e.g., `timeout='None'`).

### 3. Modal Inputs

Define inputs in modals as follows:

- **label**: The label displayed next to the input field (e.g., `label='Your Input'`).
- **placeholder**: Placeholder text for the input field (optional).
- **type**: The type of input (e.g., `short`, `paragraph`, `long`).

**Input Requirements:**

1. **Unique Labels**: Input labels should be unique within the modal.
2. **Correct Types**: Use the appropriate data types for inputs (e.g., `short`, `paragraph`, `long`).

### 4. Modal Actions

Handle modal submissions using the following:

- **Submit Action**: Define what happens when the modal is submitted. Use the `<on_submit>` tag.
- **Response Messages**: Use the `<response>` tag with `type='message'` to specify the reply message.
- **Ephemeral Responses**: Use `<ephemeral>true</ephemeral>` to make the response visible only to the user who submitted the modal.

### 5. Example Modal Definitions

Here are practical examples for common modal setups:

- **Basic Modal**

  ```xml
  <modals>
    <basic_modal title="Basic Modal">
      <inputs>
        <input label="Input" placeholder="Type here" type="short"/>
      </inputs>
      <on_submit>
        <response type='message'>
          <content>Thank you for your input: {inp(Input)}</content>
          <ephemeral>true</ephemeral>
        </response>
      </on_submit>
    </basic_modal>
  </modals>
  ```

- **Detailed Report Modal**

  ```xml
  <modals>
    <report_modal title="Report Issue">
      <inputs>
        <input label="Report reason" placeholder="Reason for the report" type="short"/>
        <input label="Description" type="paragraph"/>
        <input label="Additional information" type="long"/>
      </inputs>
      <on_submit>
        <response type='message'>
          <content>Report submitted. Additional information: {inp(Additional information)}</content>
          <ephemeral>true</ephemeral>
        </response>
      </on_submit>
    </report_modal>
  </modals>
  ```

### 6. Customizing Modal Behavior

Customize modal behavior with:

- **Dynamic Responses**: Use placeholders to customize responses based on modal inputs.
- **Conditional Logic**: Implement conditional logic within modal actions based on input values or modal types.

### 7. Troubleshooting Modals

Common issues and resolutions:

- **Modal Not Displaying**: Ensure the modal is correctly specified in the XML and that the bot has the necessary permissions.
- **Invalid Input Types**: Verify that input types match the expected values in the XML.

### 8. Best Practices

Tips for effectively using modals:

- **Organize Modals**: Keep modal definitions well-organized for easier management and debugging.
- **Optimize Performance**: Avoid overly complex logic in modal actions to maintain optimal performance.
- **Test Thoroughly**: Test modals in a development environment before deploying them.

### 9. Reporting Issues

If you encounter errors or unexpected behavior related to modals, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Modal Configuration**: The XML configuration of the modal causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
