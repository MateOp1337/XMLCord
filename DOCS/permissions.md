# XMLCord Docs | Permissions

*New in version a1.0.2*

### 1. Defining Permissions

Permissions are used to specify the required privileges for executing certain commands or actions. Define permissions within the `<permissions>` tag in your XML configuration. Example:

```xml
<commands>
  <restricted_command>
    <permissions manage_roles='true'>
      <administrator value='true'/>
    </permissions>
    <reply_message>
      <content>Command executed with the required permissions.</content>
    </reply_message>
  </restricted_command>
</commands>
```

### 2. Available Permission Attributes

Here are the attributes and elements you can use for permissions in XMLCord:

- **manage_roles**: Specifies if the command requires the ability to manage roles (e.g., `manage_roles='true'`).
- **administrator**: Specifies if the command requires administrator privileges (e.g., `<administrator value='true'/>`).
- **everyone**: Specifies if the command can be used by everyone (e.g., `<everyone value='true'/>`).

### 3. Permission Attributes and Values

Permissions can be defined in various ways. Below are all the supported formats:

#### 3.1. Basic Permissions

- **manage_roles**: Indicates if role management is required.

  ```xml
  <permissions manage_roles='true'/>
  ```

- **administrator**: Indicates if administrator privileges are required.

  ```xml
  <permissions>
    <administrator value='true'/>
  </permissions>
  ```

#### 3.2. Mixed Permissions

You can combine multiple permission types:

- **Manage Roles and Administrator**

  ```xml
  <permissions manage_roles='true'>
    <administrator value='true'/>
  </permissions>
  ```

### 4. Handling Permissions

Handle permission checks using the following:

- **Command Execution**: Verify if the user has the required permissions before executing the command.
- **Error Messages**: Use appropriate error messages if the user lacks the required permissions.

### 5. Example Permission Definitions

Here are practical examples for different permission setups:

- **Administrator Command**

  ```xml
  <commands>
    <admin_command>
      <permissions>
        <administrator value='true'/>
      </permissions>
      <reply_message>
        <content>Only administrators can execute this command.</content>
      </reply_message>
    </admin_command>
  </commands>
  ```

- **Role Management Command**

  ```xml
  <commands>
    <manage_roles_command>
      <permissions manage_roles='true'/>
      <reply_message>
        <content>Command executed with role management permissions.</content>
      </reply_message>
    </manage_roles_command>
  </commands>
  ```

### 6. Customizing Permission Behavior

Customize permission behavior with:

- **Dynamic Checks**: Implement dynamic permission checks based on user roles or command context.
- **Conditional Logic**: Use conditional logic within commands based on permissions or roles.

### 7. Troubleshooting Permissions

Common issues and resolutions:

- **Permission Denied**: Ensure the command or action has the correct permission settings and that users have the required permissions.
- **Permission Errors**: Verify that the permission attributes and values are correctly defined in the XML configuration.

### 8. Best Practices

Tips for effectively managing permissions:

- **Clear Definitions**: Clearly define required permissions for each command to avoid confusion.
- **Minimal Permissions**: Grant the minimum permissions required for command execution to maintain security.
- **Test Thoroughly**: Test permission setups in a development environment before deploying them.

### 9. Reporting Issues

If you encounter errors or unexpected behavior related to permissions, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Permission Configuration**: The XML configuration of the permissions causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
