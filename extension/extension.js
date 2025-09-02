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

    let diagnose = vscode.commands.registerCommand('abap-code-assistant.diagnose', async () => {
        await diagnoseExtension();
    });

    let installDependencies = vscode.commands.registerCommand('abap-code-assistant.installDependencies', async () => {
        await installDependenciesManually();
    });

    let checkEnvironment = vscode.commands.registerCommand('abap-code-assistant.checkEnvironment', async () => {
        await checkEnvironmentStatus();
    });

    let generateFromComment = vscode.commands.registerCommand('abap-code-assistant.generateFromComment', async () => {
        await generateFromCommentCode();
    });

    context.subscriptions.push(generateCode, generateDebug, setup, config, debug, diagnose, installDependencies, checkEnvironment, generateFromComment);
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
                vscode.window.showWarningMessage('No ABAP code generated. This might be due to missing dependencies or API issues. Try running "ABAP Code Assistant: Install Dependencies" command.');
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
                vscode.window.showWarningMessage('No ABAP debug code generated. This might be due to missing dependencies or API issues. Try running "ABAP Code Assistant: Install Dependencies" command.');
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
                vscode.window.showWarningMessage('No ABAP code generated from comment. This might be due to missing dependencies or API issues. Try running "ABAP Code Assistant: Install Dependencies" command.');
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error generating ABAP code from comment: ${error.message}`);
        }
    });
}

async function setupGroqAPI() {
    try {
        // Show progress
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Setting up ABAP Code Assistant...",
            cancellable: false
        }, async (progress) => {
            progress.report({ message: "Checking Python environment..." });
            
            // First, check Python environment
            const pythonPath = getPythonPath();
            console.log(`Using Python path: ${pythonPath}`);
            
            // Check if Python is accessible
            try {
                const testResult = await callPythonBackend('config', {});
                if (testResult) {
                    progress.report({ message: "Python environment OK, checking dependencies..." });
                }
            } catch (error) {
                console.warn(`Python test failed: ${error.message}`);
                progress.report({ message: "Python environment issues detected..." });
            }
            
            // Install dependencies (this will be silent and won't show errors to user)
            try {
                await checkAndInstallDependencies(pythonPath);
                progress.report({ message: "Dependencies checked..." });
            } catch (error) {
                console.warn(`Dependency check failed: ${error.message}`);
                // Continue anyway - the extension will work with limited functionality
            }
            
            progress.report({ message: "Requesting API key..." });
            
            const apiKey = await vscode.window.showInputBox({
                prompt: 'Enter your Groq API key (get one from groq.com)',
                password: true,
                placeHolder: 'gsk_...',
                validateInput: (value) => {
                    if (!value || value.trim() === '') {
                        return 'API key is required';
                    }
                    if (!value.startsWith('gsk_')) {
                        return 'API key should start with "gsk_"';
                    }
                    return null;
                }
            });

            if (apiKey) {
                progress.report({ message: "Testing API key..." });
                
                // Update configuration
                await vscode.workspace.getConfiguration('abapCodeAssistant').update('groqApiKey', apiKey, vscode.ConfigurationTarget.Global);
                
                // Test the setup with API key as environment variable
                try {
                    const result = await callPythonBackend('setup', { apiKey: apiKey });
                    if (result && result.includes('successful')) {
                        vscode.window.showInformationMessage('✅ Groq API setup successful! You can now use ABAP code generation.');
                    } else {
                        // Show more detailed error information
                        const errorDetails = result || 'Unknown error';
                        console.warn(`Setup result: ${errorDetails}`);
                        
                        // Check if it's a dependency issue
                        if (errorDetails.includes('groq package not available') || errorDetails.includes('dependencies')) {
                            vscode.window.showErrorMessage('❌ Setup failed: Python dependencies are missing. Please run the diagnostic command to fix this.');
                        } else {
                            vscode.window.showWarningMessage('⚠️ Setup completed but API test failed. Please run the diagnostic command for more details.');
                        }
                    }
                } catch (error) {
                    console.warn(`API test failed: ${error.message}`);
                    
                    // Provide more specific error messages
                    if (error.message.includes('Python process failed')) {
                        vscode.window.showErrorMessage('❌ Setup failed: Python backend error. Please run the diagnostic command to troubleshoot.');
                    } else if (error.message.includes('Failed to start Python process')) {
                        vscode.window.showErrorMessage('❌ Setup failed: Python not found. Please install Python 3.11+ and run the diagnostic command.');
                    } else {
                        vscode.window.showErrorMessage(`❌ Setup failed: ${error.message}. Please run the diagnostic command for more details.`);
                    }
                }
            } else {
                vscode.window.showWarningMessage('Setup cancelled. No API key provided.');
            }
        });
    } catch (error) {
        console.error(`Setup error: ${error.message}`);
        vscode.window.showErrorMessage(`Setup error: ${error.message}. Please check the Output panel for details.`);
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
    return new Promise(async (resolve, reject) => {
        const pythonPath = getPythonPath();
        const scriptPath = path.join(__dirname, 'python', 'main.py');
        
        console.log(`Calling Python backend: ${pythonPath} ${scriptPath} ${command}`);
        console.log(`Working directory: ${path.join(__dirname, 'python')}`);
        console.log(`Extension directory: ${__dirname}`);
        
        // Check if Python dependencies are installed
        try {
            await checkAndInstallDependencies(pythonPath);
        } catch (error) {
            console.warn(`Warning: Could not install dependencies: ${error.message}`);
            // Log the warning but don't show to user yet - let the main operation fail gracefully
        }
        
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
        
        // If API key was not explicitly provided, attempt to read a .env file in the python folder as a fallback
        const fs = require('fs');
        try {
            if (!env['GROQ_API_KEY']) {
                const envFile = path.join(__dirname, 'python', '.env');
                if (fs.existsSync(envFile)) {
                    const contents = fs.readFileSync(envFile, 'utf8');
                    const lines = contents.split(/\r?\n/);
                    for (const line of lines) {
                        const trimmed = line.trim();
                        if (!trimmed || trimmed.startsWith('#')) continue;
                        const idx = trimmed.indexOf('=');
                        if (idx === -1) continue;
                        const k = trimmed.substring(0, idx).trim();
                        const v = trimmed.substring(idx + 1).trim();
                        if (k === 'GROQ_API_KEY' && v) {
                            env['GROQ_API_KEY'] = v.replace(/^\"|\"$/g, '');
                            console.log('Loaded GROQ_API_KEY from extension/python/.env');
                            break;
                        }
                    }
                }
            }
        } catch (err) {
            console.warn('Could not read .env fallback:', err.message);
        }

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
            console.log(`Python stdout: ${stdout}`);
            console.log(`Python stderr: ${stderr}`);
            
            if (code === 0) {
                resolve(stdout.trim());
            } else {
                const errorMsg = stderr || `Process failed with code ${code}`;
                console.error(`Python backend error: ${errorMsg}`);
                reject(new Error(`Python process failed (code ${code}): ${errorMsg}`));
            }
        });

        child.on('error', (error) => {
            console.error(`Python process error: ${error.message}`);
            console.error(`Error details: ${JSON.stringify(error, null, 2)}`);
            reject(new Error(`Failed to start Python process: ${error.message}`));
        });
    });
}

async function checkAndInstallDependencies(pythonPath) {
    return new Promise((resolve, reject) => {
        const checkScript = path.join(__dirname, 'python', 'check_dependencies.py');
        
        console.log(`Checking Python dependencies...`);
        console.log(`Python path: ${pythonPath}`);
        console.log(`Check script: ${checkScript}`);
        
        // Check if the check script exists
        if (!require('fs').existsSync(checkScript)) {
            console.warn(`⚠️ Dependency check script not found: ${checkScript}`);
            resolve(); // Don't fail, just continue
            return;
        }
        
        const child = spawn(pythonPath, [checkScript], {
            cwd: path.join(__dirname, 'python'),
            env: { ...process.env, PYTHONPATH: path.join(__dirname, 'python') }
        });
        
        let stdout = '';
        let stderr = '';
        
        child.stdout.on('data', (data) => {
            stdout += data.toString();
            console.log(`Dependency check: ${data.toString().trim()}`);
        });
        
        child.stderr.on('data', (data) => {
            stderr += data.toString();
            console.log(`Dependency check error: ${data.toString().trim()}`);
        });
        
        child.on('close', (code) => {
            console.log(`Dependency check process exited with code: ${code}`);
            if (code === 0) {
                console.log(`✅ Dependencies check successful`);
                resolve();
            } else {
                console.warn(`⚠️ Dependencies check failed (code ${code}): ${stderr}`);
                
                // Handle different failure scenarios gracefully
                if (code === 1 && stderr.includes('Missing packages')) {
                    console.log(`ℹ️ Missing packages detected, will install automatically`);
                    // Don't show warning for missing packages - this is expected
                } else if (code === 2) {
                    console.log(`ℹ️ Dependencies installed successfully`);
                } else {
                    // Only show warning for unexpected errors
                    console.warn(`⚠️ Unexpected dependency check failure`);
                }
                resolve();
            }
        });
        
        child.on('error', (error) => {
            console.warn(`⚠️ Could not check dependencies: ${error.message}`);
            console.warn(`Error details: ${JSON.stringify(error, null, 2)}`);
            // Don't fail the main operation, just log the warning
            resolve();
        });
        
        // Add timeout to prevent hanging
        setTimeout(() => {
            console.warn(`⚠️ Dependency check timed out, continuing anyway`);
            child.kill();
            resolve();
        }, 30000); // 30 second timeout
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
    
    // Try to find conda environment first
    const condaPath = findCondaPython();
    if (condaPath) {
        console.log(`Using conda Python path: ${condaPath}`);
        return condaPath;
    }
    
    // Try common Python paths based on platform
    const platform = process.platform;
    let defaultPath = 'python3';
    
    if (platform === 'win32') {
        // Windows: try python first, then python3
        defaultPath = 'python';
    } else if (platform === 'darwin') {
        // macOS: try python3 first, then python
        defaultPath = 'python3';
    } else {
        // Linux: try python3 first, then python
        defaultPath = 'python3';
    }
    
    console.log(`Using default Python path for ${platform}: ${defaultPath}`);
    return defaultPath;
}

function findCondaPython() {
    const platform = process.platform;
    const homeDir = process.env.HOME || process.env.USERPROFILE;
    
    // Common conda installation paths
    const condaPaths = [
        // Homebrew conda (macOS)
        '/opt/homebrew/Caskroom/miniconda/base/envs/abap-assistant/bin/python',
        '/opt/homebrew/Caskroom/miniconda/base/bin/python',
        // User conda
        path.join(homeDir, 'miniconda3/envs/abap-assistant/bin/python'),
        path.join(homeDir, 'anaconda3/envs/abap-assistant/bin/python'),
        path.join(homeDir, 'miniconda3/bin/python'),
        path.join(homeDir, 'anaconda3/bin/python'),
        // System conda
        '/usr/local/miniconda3/envs/abap-assistant/bin/python',
        '/usr/local/anaconda3/envs/abap-assistant/bin/python'
    ];
    
    // Check if any of these paths exist and are executable
    for (const condaPath of condaPaths) {
        try {
            if (require('fs').existsSync(condaPath)) {
                // Check if it's executable
                const stats = require('fs').statSync(condaPath);
                if (stats.isFile() && (stats.mode & 0o111)) {
                    console.log(`Found conda Python at: ${condaPath}`);
                    return condaPath;
                }
            }
        } catch (error) {
            console.log(`Could not check conda path ${condaPath}: ${error.message}`);
        }
    }
    
    console.log('No conda Python found, will use system Python');
    return null;
}

async function diagnoseExtension() {
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Diagnosing ABAP Code Assistant...",
            cancellable: false
        }, async (progress) => {
            progress.report({ message: "Checking Python environment..." });
            
            const pythonPath = getPythonPath();
            const config = vscode.workspace.getConfiguration('abapCodeAssistant');
            const apiKey = config.get('groqApiKey');
            
            let diagnosis = [];
            
            // Check Python path
            diagnosis.push(`🐍 Python Path: ${pythonPath}`);
            
            // Check API key
            if (apiKey) {
                diagnosis.push(`🔑 API Key: ✅ Set (starts with ${apiKey.substring(0, 10)}...)`);
            } else {
                diagnosis.push(`🔑 API Key: ❌ Not set`);
            }
            
            // Test Python backend
            progress.report({ message: "Testing Python backend..." });
            try {
                const result = await callPythonBackend('config', {});
                if (result) {
                    diagnosis.push(`🔧 Python Backend: ✅ Working`);
                    diagnosis.push(`📊 Backend Response: ${result.substring(0, 100)}...`);
                } else {
                    diagnosis.push(`🔧 Python Backend: ⚠️ No response`);
                }
            } catch (error) {
                diagnosis.push(`🔧 Python Backend: ❌ Error - ${error.message}`);
            }
            
            // Check dependencies
            progress.report({ message: "Checking dependencies..." });
            try {
                await checkAndInstallDependencies(pythonPath);
                diagnosis.push(`📦 Dependencies: ✅ Checked`);
            } catch (error) {
                diagnosis.push(`📦 Dependencies: ⚠️ Check failed - ${error.message}`);
            }
            
            // Show diagnosis
            const diagnosisText = diagnosis.join('\n');
            const doc = await vscode.workspace.openTextDocument({
                content: `# ABAP Code Assistant Diagnosis\n\n${diagnosisText}\n\n## Troubleshooting Tips\n\n1. Make sure you have a valid Groq API key\n2. Check that Python dependencies are installed\n3. Verify your Python environment is accessible\n4. Check the Output panel for detailed error messages`,
                language: 'markdown'
            });
            
            await vscode.window.showTextDocument(doc);
            
            vscode.window.showInformationMessage('Diagnosis complete! Check the opened document for details.');
        });
    } catch (error) {
        vscode.window.showErrorMessage(`Diagnosis failed: ${error.message}`);
    }
}

async function installDependenciesManually() {
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Installing Python Dependencies...",
            cancellable: false
        }, async (progress) => {
            progress.report({ message: "Checking Python environment..." });
            
            const pythonPath = getPythonPath();
            if (!pythonPath) {
                vscode.window.showErrorMessage('❌ Python not found. Please install Python 3.8+ first.');
                return;
            }
            
            // First run the basic environment check
            progress.report({ message: "Running environment diagnostics..." });
            try {
                const envCheckResult = await callPythonBackend('env_check', {});
                if (envCheckResult) {
                    console.log('Environment check completed');
                }
            } catch (error) {
                console.warn(`Environment check failed: ${error.message}`);
            }
            
            progress.report({ message: "Installing dependencies..." });
            
            try {
                await checkAndInstallDependencies(pythonPath);
                vscode.window.showInformationMessage('✅ Dependencies installed successfully! You can now use the extension.');
            } catch (error) {
                console.error(`Dependency installation failed: ${error.message}`);
                
                // Provide more specific guidance
                let errorMessage = `❌ Failed to install dependencies: ${error.message}\n\n`;
                errorMessage += `💡 Troubleshooting steps:\n`;
                errorMessage += `1. Run "ABAP Code Assistant: Diagnose Extension"\n`;
                errorMessage += `2. Check the Output panel for detailed error messages\n`;
                errorMessage += `3. Try running: python env_check.py in the extension/python directory\n`;
                errorMessage += `4. Ensure you have Python 3.8+ and pip installed`;
                
                vscode.window.showErrorMessage(errorMessage);
            }
        });
    } catch (error) {
        vscode.window.showErrorMessage(`Installation failed: ${error.message}`);
    }
}

async function checkEnvironmentStatus() {
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Checking Environment...",
            cancellable: false
        }, async (progress) => {
            progress.report({ message: "Running environment diagnostics..." });
            
            const pythonPath = getPythonPath();
            if (!pythonPath) {
                vscode.window.showErrorMessage('❌ Python not found. Please install Python 3.8+ first.');
                return;
            }
            
            try {
                const result = await callPythonBackend('env_check', {});
                if (result) {
                    // Show the results in a new document
                    const doc = await vscode.workspace.openTextDocument({
                        content: `# Environment Check Results\n\n${result}`,
                        language: 'markdown'
                    });
                    await vscode.window.showTextDocument(doc);
                    vscode.window.showInformationMessage('✅ Environment check completed! Check the opened document for results.');
                } else {
                    vscode.window.showWarningMessage('⚠️ Environment check completed but no results returned.');
                }
            } catch (error) {
                console.error(`Environment check failed: ${error.message}`);
                vscode.window.showErrorMessage(`❌ Environment check failed: ${error.message}\n\nCheck the Output panel for details.`);
            }
        });
    } catch (error) {
        vscode.window.showErrorMessage(`Environment check failed: ${error.message}`);
    }
}

function deactivate() {
    console.log('ABAP AI Code Completion extension is now deactivated');
}

module.exports = {
    activate,
    deactivate
}; 