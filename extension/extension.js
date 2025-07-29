const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('ABAP Code Assistant extension is now active!');

    // Register commands
    let generateCode = vscode.commands.registerCommand('abap-code-assistant.generateCode', async () => {
        await generateABAPCode();
    });

    let generateDebug = vscode.commands.registerCommand('abap-code-assistant.generateDebug', async () => {
        await generateABAPDebugCode();
    });

    let setup = vscode.commands.registerCommand('abap-code-assistant.setup', async () => {
        await setupGroqAPI();
    });

    let config = vscode.commands.registerCommand('abap-code-assistant.config', async () => {
        await showConfiguration();
    });

    let debug = vscode.commands.registerCommand('abap-code-assistant.debug', async () => {
        await debugApiKey();
    });

    let generateFromComment = vscode.commands.registerCommand('abap-code-assistant.generateFromComment', async () => {
        await generateFromCommentCode();
    });

    context.subscriptions.push(generateCode, generateDebug, setup, config, debug, generateFromComment);
}

async function generateABAPCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'abap') {
        vscode.window.showWarningMessage('This command is only available for ABAP files');
        return;
    }

    const position = editor.selection.active;
    const text = document.getText();
    const lines = text.split('\n');

    // Get context around cursor
    const lineNumber = position.line;
    const currentLine = lines[lineNumber] || '';
    const prefix = lines.slice(0, lineNumber).join('\n') + '\n' + currentLine.substring(0, position.character);
    const suffix = currentLine.substring(position.character) + '\n' + lines.slice(lineNumber + 1).join('\n');

    // Show progress
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Generating ABAP code...",
        cancellable: true
    }, async (progress, token) => {
        try {
            // Get API key from VS Code settings
            const config = vscode.workspace.getConfiguration('abapCodeAssistant');
            const apiKey = config.get('groqApiKey');
            
            console.log(`Retrieved API key from settings: ${apiKey ? 'YES' : 'NO'}`);
            if (apiKey) {
                console.log(`API key starts with: ${apiKey.substring(0, 10)}...`);
            }
            
            if (!apiKey) {
                vscode.window.showErrorMessage('Please set up your Groq API key first. Use "ABAP Code Assistant: Setup Groq API" command.');
                return;
            }
            
            const completion = await callPythonBackend('generate', {
                prefix: prefix,
                suffix: suffix,
                file: document.fileName,
                language: 'abap',
                mode: 'code',
                apiKey: apiKey
            });

            if (completion && completion.trim()) {
                // Insert completion at cursor position
                const edit = new vscode.WorkspaceEdit();
                edit.insert(document.uri, position, completion);
                await vscode.workspace.applyEdit(edit);
                
                vscode.window.showInformationMessage('ABAP code generated successfully!');
            } else {
                vscode.window.showWarningMessage('No ABAP code generated');
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error generating ABAP code: ${error.message}`);
        }
    });
}

async function generateABAPDebugCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'abap') {
        vscode.window.showWarningMessage('This command is only available for ABAP files');
        return;
    }

    const position = editor.selection.active;
    const text = document.getText();
    const lines = text.split('\n');

    // Get context around cursor
    const lineNumber = position.line;
    const currentLine = lines[lineNumber] || '';
    const prefix = lines.slice(0, lineNumber).join('\n') + '\n' + currentLine.substring(0, position.character);
    const suffix = currentLine.substring(position.character) + '\n' + lines.slice(lineNumber + 1).join('\n');

    // Show progress
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Generating ABAP debug code...",
        cancellable: true
            }, async (progress, token) => {
        try {
            // Get API key from VS Code settings
            const config = vscode.workspace.getConfiguration('abapCodeAssistant');
            const apiKey = config.get('groqApiKey');
            
            console.log(`Retrieved API key from settings: ${apiKey ? 'YES' : 'NO'}`);
            if (apiKey) {
                console.log(`API key starts with: ${apiKey.substring(0, 10)}...`);
            }
            
            if (!apiKey) {
                vscode.window.showErrorMessage('Please set up your Groq API key first. Use "ABAP Code Assistant: Setup Groq API" command.');
                return;
            }
            
            const debugCode = await callPythonBackend('generate', {
                prefix: prefix,
                suffix: suffix,
                file: document.fileName,
                language: 'abap',
                mode: 'debug',
                apiKey: apiKey
            });

            if (debugCode && debugCode.trim()) {
                // Insert debug code at cursor position
                const edit = new vscode.WorkspaceEdit();
                edit.insert(document.uri, position, debugCode);
                await vscode.workspace.applyEdit(edit);
                
                vscode.window.showInformationMessage('ABAP debug code generated successfully!');
            } else {
                vscode.window.showWarningMessage('No ABAP debug code generated');
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error generating ABAP debug code: ${error.message}`);
        }
    });
}

async function generateFromCommentCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'abap') {
        vscode.window.showWarningMessage('This command is only available for ABAP files');
        return;
    }

    const selection = editor.selection;
    if (selection.isEmpty) {
        vscode.window.showWarningMessage('Please select a comment to generate code from');
        return;
    }

    const selectedText = document.getText(selection);
    const text = document.getText();
    const lines = text.split('\n');

    // Get context around the selection
    const startLine = selection.start.line;
    const endLine = selection.end.line;
    
    // Get prefix (code before the comment)
    const prefix = lines.slice(0, startLine).join('\n');
    
    // Get suffix (code after the comment)
    const suffix = lines.slice(endLine + 1).join('\n');

    // Show progress
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Generating ABAP code from comment...",
        cancellable: true
            }, async (progress, token) => {
        try {
            // Get API key from VS Code settings
            const config = vscode.workspace.getConfiguration('abapCodeAssistant');
            const apiKey = config.get('groqApiKey');
            
            console.log(`Retrieved API key from settings: ${apiKey ? 'YES' : 'NO'}`);
            if (apiKey) {
                console.log(`API key starts with: ${apiKey.substring(0, 10)}...`);
            }
            
            if (!apiKey) {
                vscode.window.showErrorMessage('Please set up your Groq API key first. Use "ABAP Code Assistant: Setup Groq API" command.');
                return;
            }
            
            const completion = await callPythonBackend('generate', {
                prefix: prefix,
                suffix: suffix,
                comment: selectedText,
                file: document.fileName,
                language: 'abap',
                mode: 'comment',
                apiKey: apiKey
            });

            if (completion && completion.trim()) {
                // Replace the selected comment with the generated code
                const edit = new vscode.WorkspaceEdit();
                edit.replace(document.uri, selection, completion);
                await vscode.workspace.applyEdit(edit);
                
                vscode.window.showInformationMessage('ABAP code generated from comment successfully!');
            } else {
                vscode.window.showWarningMessage('No ABAP code generated from comment');
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error generating ABAP code from comment: ${error.message}`);
        }
    });
}

async function setupGroqAPI() {
    try {
        const apiKey = await vscode.window.showInputBox({
            prompt: 'Enter your Groq API key',
            password: true,
            placeHolder: 'gsk_...'
        });

        if (apiKey) {
            // Update configuration
            await vscode.workspace.getConfiguration('abapCodeAssistant').update('groqApiKey', apiKey, vscode.ConfigurationTarget.Global);
            
            // Test the setup with API key as environment variable
            const result = await callPythonBackend('setup', { apiKey: apiKey });
            if (result && result.includes('successful')) {
                vscode.window.showInformationMessage('Groq API setup successful!');
            } else {
                vscode.window.showErrorMessage('Setup failed. Please check your API key.');
            }
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Setup error: ${error.message}`);
    }
}

async function showConfiguration() {
    try {
        // Get API key from VS Code settings
        const vsCodeConfig = vscode.workspace.getConfiguration('abapCodeAssistant');
        const apiKey = vsCodeConfig.get('groqApiKey');
        
        // Pass API key to config command
        const config = await callPythonBackend('config', { apiKey: apiKey || '' });
        if (config) {
            // Create and show a new document with configuration
            const document = await vscode.workspace.openTextDocument({
                content: config,
                language: 'json'
            });
            await vscode.window.showTextDocument(document);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error showing configuration: ${error.message}`);
    }
}

async function debugApiKey() {
    try {
        console.log('🔍 Debugging API Key...');
        
        // Check VS Code settings
        const config = vscode.workspace.getConfiguration('abapCodeAssistant');
        const apiKey = config.get('groqApiKey');
        
        console.log(`API key in settings: ${apiKey ? 'YES' : 'NO'}`);
        if (apiKey) {
            console.log(`API key starts with: ${apiKey.substring(0, 10)}...`);
        }
        
        // Test Python backend with API key
        if (apiKey) {
            console.log('Testing Python backend with API key...');
            const result = await callPythonBackend('generate', {
                prefix: 'REPORT z_test.',
                suffix: '\nEND-OF-SELECTION.',
                apiKey: apiKey
            });
            
            if (result) {
                console.log('✅ Python backend test successful');
                vscode.window.showInformationMessage('Debug: API key is working correctly!');
            } else {
                console.log('❌ Python backend test failed');
                vscode.window.showErrorMessage('Debug: API key is not working');
            }
        } else {
            console.log('❌ No API key found in settings');
            vscode.window.showErrorMessage('Debug: No API key found in settings');
        }
        
    } catch (error) {
        console.log(`❌ Debug error: ${error.message}`);
        vscode.window.showErrorMessage(`Debug error: ${error.message}`);
    }
}

async function callPythonBackend(command, args = {}) {
    return new Promise((resolve, reject) => {
        const pythonPath = getPythonPath();
        const scriptPath = path.join(__dirname, 'python', 'main.py');
        
        console.log(`Calling Python backend: ${pythonPath} ${scriptPath} ${command}`);
        console.log(`Working directory: ${path.join(__dirname, 'python')}`);
        
        const processArgs = [scriptPath, command];
        
        // Add arguments as environment variables
        const env = { ...process.env };
        Object.entries(args).forEach(([key, value]) => {
            if (key === 'apiKey') {
                // Special handling for API key - Python backend expects GROQ_API_KEY
                env['GROQ_API_KEY'] = value;
                console.log(`Setting GROQ_API_KEY environment variable: ${value.substring(0, 10)}...`);
            } else {
                env[`LACC_${key.toUpperCase()}`] = value;
            }
        });
        
        console.log(`Environment variables: ${Object.keys(env).filter(k => k.includes('GROQ') || k.includes('LACC')).join(', ')}`);
        console.log(`GROQ_API_KEY set: ${env['GROQ_API_KEY'] ? 'YES' : 'NO'}`);

        const child = spawn(pythonPath, processArgs, {
            env: env,
            cwd: path.join(__dirname, 'python')
        });

        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (data) => {
            stdout += data.toString();
            console.log(`Python stdout: ${data.toString()}`);
        });

        child.stderr.on('data', (data) => {
            stderr += data.toString();
            console.log(`Python stderr: ${data.toString()}`);
        });

        child.on('close', (code) => {
            console.log(`Python process exited with code: ${code}`);
            if (code === 0) {
                resolve(stdout.trim());
            } else {
                reject(new Error(`Python process failed (code ${code}): ${stderr}`));
            }
        });

        child.on('error', (error) => {
            console.error(`Python process error: ${error.message}`);
            reject(new Error(`Failed to start Python process: ${error.message}`));
        });
    });
}

function getPythonPath() {
    // Try to get Python path from VS Code settings
    const config = vscode.workspace.getConfiguration('python');
    const pythonPath = config.get('pythonPath') || config.get('defaultInterpreterPath');
    
    if (pythonPath) {
        console.log(`Using Python path from VS Code settings: ${pythonPath}`);
        return pythonPath;
    }
    
    // Try common Python paths
    const commonPaths = [
        'python3',
        'python',
        '/usr/bin/python3',
        '/usr/bin/python',
        '/opt/anaconda3/bin/python',
        '/opt/homebrew/bin/python3',
        '/opt/homebrew/bin/python'
    ];
    
    // For now, return python3 as it's most common on macOS
    const defaultPath = 'python3';
    console.log(`Using default Python path: ${defaultPath}`);
    return defaultPath;
}

function deactivate() {
    console.log('ABAP AI Code Completion extension is now deactivated');
}

module.exports = {
    activate,
    deactivate
}; 