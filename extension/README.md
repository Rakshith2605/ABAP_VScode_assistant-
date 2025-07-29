# ABAP Code Assistant - VS Code Extension

A VS Code extension that provides AI-powered ABAP code assistant with code generation and debugging using the Groq API.

## Features

- **ABAP Code Generation**: Generate ABAP code following SAP best practices
- **ABAP Debug Code Generation**: Generate debugging code with proper ABAP debugging patterns
- **Comment-Based Code Generation**: Generate code from comments with `Ctrl+Shift+G` when text is selected
- **ABAP Syntax Highlighting**: Full ABAP language support with syntax highlighting
- **Groq API Integration**: Uses Groq's fast inference API for code generation
- **SAP Best Practices**: Follows SAP coding standards and guidelines
- **Keyboard Shortcuts**: Quick access with `Ctrl+Shift+G` and `Ctrl+Shift+D`

## Demo

![ABAP Code Assistant Demo](publi/abap_vid.gif)

*Watch the ABAP Code Assistant in action - generating code from comments seamlessly!*

*Note: The demo GIF shows the comment-based code generation feature in action. Select a comment and press Ctrl+Shift+G to see the magic happen!*

## Usage

### Generate ABAP Code

1. **Open an ABAP file** (`.abap`, `.sap`, `.sapabap`)
2. **Position your cursor** where you want code completion
3. **Press `Ctrl+Shift+G`** (or `Cmd+Shift+G` on Mac)
4. **Wait for generation** - the extension will analyze context and generate ABAP code
5. **Review and accept** the generated code

### Generate ABAP Debug Code

1. **Open an ABAP file**
2. **Position your cursor** where you want debug code
3. **Press `Ctrl+Shift+D`** (or `Cmd+Shift+D` on Mac)
4. **Wait for generation** - the extension will generate ABAP debugging code
5. **Review and accept** the generated debug code

### Generate Code from Comment

1. **Open an ABAP file**
2. **Type a comment** describing what you want to implement
3. **Select the comment** (highlight it)
4. **Press `Ctrl+Shift+G`** - the comment will be replaced with generated code
5. **Review and accept** the generated code

### Example

```abap
REPORT z_example.
DATA: lv_a TYPE i,
      lv_b TYPE i.

START-OF-SELECTION.
  [Select this comment: "* calculate sum"]
  [Press Ctrl+Shift+G]
  [Gets replaced with:]
  lv_a = 5.
  lv_b = 10.
  lv_sum = lv_a + lv_b.
  WRITE: / 'The sum of', lv_a, 'and', lv_b, 'is', lv_sum.
```

### Commands

- **Generate ABAP Code** (`Ctrl+Shift+G`): Generate ABAP code at cursor
- **Generate ABAP Debug Code** (`Ctrl+Shift+D`): Generate debug code at cursor
- **Generate Code from Comment** (`Ctrl+Shift+G` with selection): Generate code from selected comment
- **Setup Groq API**: Configure your API key
- **Show Configuration**: Display current settings

## ABAP Features

### Code Generation

The extension generates ABAP code that:
- Follows SAP coding standards
- Uses proper ABAP syntax and keywords
- Includes proper error handling
- Uses meaningful variable names
- Includes comments where appropriate
- Follows the context and completes code logically

### Debug Code Generation

The extension generates ABAP debug code that:
- Uses proper ABAP debugging statements (BREAK-POINT, WRITE, etc.)
- Includes variable inspection code
- Uses proper ABAP debugging patterns
- Includes performance monitoring if applicable
- Uses meaningful debug messages
- Follows SAP debugging guidelines

### Common ABAP Debug Patterns

- **BREAK-POINT**: For breakpoints
- **WRITE**: For output statements
- **DESCRIBE TABLE**: For table inspection
- **SY_TABIX**: For loop index
- **SY_SUBRC**: For return codes
- **GET TIME**: For performance timing

## Installation

1. **Download the extension**: `abap-code-assistant-1.0.0.vsix`
2. **Open VS Code** and go to Extensions (`Ctrl+Shift+X`)
3. **Click "..."** in the Extensions panel and select "Install from VSIX..."
4. **Select the extension package**
5. **Set up your Groq API key** using "ABAP Code Assistant: Setup Groq API"

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
- Try a different model or adjust temperature

### Issue: ABAP syntax not recognized
- Make sure the file has `.abap`, `.sap`, or `.sapabap` extension
- Check that the ABAP language support is enabled

## ABAP Language Support

The extension provides:
- **Syntax Highlighting**: Full ABAP syntax support
- **Language Configuration**: Proper ABAP indentation and brackets
- **File Extensions**: `.abap`, `.sap`, `.sapabap`
- **Keywords**: ABAP keywords and operators
- **Comments**: Support for `*` and `"` comments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with ABAP code
5. Submit a pull request

## License

This extension is licensed under the same license as the main project.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in VS Code's Developer Console
3. Test with the provided ABAP example files
4. Open an issue on the project repository

## Example Usage

### ABAP Code Generation

```abap
* Position cursor here and press Ctrl+Shift+G
FORM get_customer_data.
  CLEAR: lt_customers, lv_count.
  
  " AI will generate code like:
  " SELECT customer_id, name, email, phone
  "   FROM customers
  "   WHERE customer_id = @p_customer
  "   INTO TABLE @lt_customers.
  "
  " IF sy-subrc = 0.
  "   lv_count = lines( lt_customers ).
  "   WRITE: / 'Found', lv_count, 'customers'.
  " ELSE.
  "   MESSAGE 'No customers found' TYPE 'E'.
  " ENDIF.
ENDFORM.
```

### ABAP Debug Code Generation

```abap
* Position cursor here and press Ctrl+Shift+D
FORM display_customer_data.
  " AI will generate debug code like:
  " BREAK-POINT.
  " WRITE: / 'Debug: Customer count =', lv_count.
  " 
  " LOOP AT lt_customers INTO ls_customer.
  "   WRITE: / 'Customer:', ls_customer-customer_id,
  "            'Name:', ls_customer-name.
  "   sy-tabix = sy-tabix.
  " ENDLOOP.
  "
  " DESCRIBE TABLE lt_customers LINES lv_count.
  " WRITE: / 'Total lines:', lv_count.
ENDFORM.
```

Happy ABAP coding! 🚀 
