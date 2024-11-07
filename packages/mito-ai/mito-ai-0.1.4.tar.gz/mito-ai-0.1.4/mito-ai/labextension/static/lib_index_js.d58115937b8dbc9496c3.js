"use strict";
(self["webpackChunkmito_ai"] = self["webpackChunkmito_ai"] || []).push([["lib_index_js"],{

/***/ "./lib/Extensions/AiChat/AiChatPlugin.js":
/*!***********************************************!*\
  !*** ./lib/Extensions/AiChat/AiChatPlugin.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _ChatWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./ChatWidget */ "./lib/Extensions/AiChat/ChatWidget.js");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../VariableManager/VariableManagerPlugin */ "./lib/Extensions/VariableManager/VariableManagerPlugin.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");







/**
 * Initialization data for the mito-ai extension.
 */
const AiChatPlugin = {
    id: 'mito_ai:plugin',
    description: 'AI chat for JupyterLab',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry, _VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_4__.IVariableManager],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, notebookTracker, palette, rendermime, variableManager, restorer) => {
        // Define a widget creator function,
        // then call it to make a new widget
        const newWidget = () => {
            // Create a blank content widget inside of a MainAreaWidget
            const chatWidget = (0,_ChatWidget__WEBPACK_IMPORTED_MODULE_5__.buildChatWidget)(app, notebookTracker, rendermime, variableManager);
            return chatWidget;
        };
        let widget = newWidget();
        // Add an application command
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT, {
            label: 'Your friendly Python Expert chat bot',
            execute: () => {
                // In order for the widget to be accessible, the widget must be:
                // 1. Created
                // 2. Added to the widget tracker
                // 3. Attatched to the frontend 
                // Step 1: Create the widget if its not already created
                if (!widget || widget.isDisposed) {
                    widget = newWidget();
                }
                // Step 2: Add the widget to the widget tracker if 
                // its not already there
                if (!tracker.has(widget)) {
                    tracker.add(widget);
                }
                // Step 3: Attatch the widget to the app if its not 
                // already there
                if (!widget.isAttached) {
                    app.shell.add(widget, 'left', { rank: 2000 });
                }
                // Now that the widget is potentially accessible, activating the 
                // widget opens the taskpane
                app.shell.activateById(widget.id);
                // Set focus on the chat input
                const chatInput = widget.node.querySelector('.chat-input');
                chatInput === null || chatInput === void 0 ? void 0 : chatInput.focus();
            }
        });
        app.commands.addKeyBinding({
            command: _commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT,
            keys: ['Accel E'],
            selector: 'body',
        });
        app.shell.add(widget, 'left', { rank: 2000 });
        // Add the command to the palette.
        palette.addItem({ command: _commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT, category: 'AI Chat' });
        // Track and restore the widget state
        let tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: widget.id
        });
        if (restorer) {
            restorer.add(widget, 'mito_ai');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (AiChatPlugin);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatHistoryManager.js":
/*!*****************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatHistoryManager.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatHistoryManager: () => (/* binding */ ChatHistoryManager)
/* harmony export */ });
/* harmony import */ var _utils_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../utils/notebook */ "./lib/utils/notebook.js");

/*
    The ChatHistoryManager is responsible for managing the AI chat history.

    It keeps track of two types of messages:
    1. aiOptimizedChatHistory: Messages sent to the AI that include things like: instructions on how to respond, the code context, etc.
    2. displayOptimizedChatHistory: Messages displayed in the chat interface that only display info the user wants to see,
    like their original input.

    TODO: In the future, we should make this its own extension that provides an interface for adding new messages to the chat history,
    creating new chats, etc. Doing so would allow us to easily append new messages from other extensions without having to do so
    by calling commands with untyped arguments.

    Whenever, the chatHistoryManager is updated, it should automatically send a message to the AI.
*/
class ChatHistoryManager {
    constructor(variableManager, notebookTracker, initialHistory) {
        this.getLastAIMessageIndex = () => {
            const displayOptimizedChatHistory = this.getDisplayOptimizedHistory();
            const aiMessageIndexes = displayOptimizedChatHistory.map((chatEntry, index) => {
                if (chatEntry.message.role === 'assistant') {
                    return index;
                }
                return undefined;
            }).filter(index => index !== undefined);
            return aiMessageIndexes[aiMessageIndexes.length - 1];
        };
        this.getLastAIMessage = () => {
            const lastAIMessagesIndex = this.getLastAIMessageIndex();
            if (!lastAIMessagesIndex) {
                return;
            }
            const displayOptimizedChatHistory = this.getDisplayOptimizedHistory();
            return displayOptimizedChatHistory[lastAIMessagesIndex];
        };
        // Initialize the history
        this.history = initialHistory || {
            aiOptimizedChatHistory: [],
            displayOptimizedChatHistory: []
        };
        // Save the variable manager
        this.variableManager = variableManager;
        // Save the notebook tracker
        this.notebookTracker = notebookTracker;
    }
    createDuplicateChatHistoryManager() {
        return new ChatHistoryManager(this.variableManager, this.notebookTracker, this.history);
    }
    getHistory() {
        return { ...this.history };
    }
    getAIOptimizedHistory() {
        return this.history.aiOptimizedChatHistory;
    }
    getDisplayOptimizedHistory() {
        return this.history.displayOptimizedChatHistory;
    }
    addChatInputMessage(input) {
        const variables = this.variableManager.variables;
        const activeCellCode = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_0__.getActiveCellCode)(this.notebookTracker);
        const aiOptimizedMessage = {
            role: 'user',
            content: `You have access to the following variables:

${variables === null || variables === void 0 ? void 0 : variables.map(variable => `${JSON.stringify(variable, null, 2)}\n`).join('')}

Complete the task below. Decide what variables to use and what changes you need to make to the active code cell. Only return the full new active code cell and a concise explanation of the changes you made.

<Reminders>

Do not: 
- Use the word "I"
- Include multiple approaches in your response
- Recreate variables that already exist

Do: 
- Use the variables that you have access to
- Keep as much of the original code as possible
- Ask for more context if you need it. 

</Reminders>

<Example>

Code in the active code cell:

\`\`\`python
import pandas as pd
loans_df = pd.read_csv('./loans.csv')
\`\`\`

Your task: convert the issue_date column to datetime.

Output:

\`\`\`python
import pandas as pd
loans_df = pd.read_csv('./loans.csv')
loans_df['issue_date'] = pd.to_datetime(loans_df['issue_date'])
\`\`\`

Use the pd.to_datetime function to convert the issue_date column to datetime.

</Example>

Code in the active code cell:

\`\`\`python
${activeCellCode}
\`\`\`

Your task: ${input}`
        };
        this.history.displayOptimizedChatHistory.push({ message: getDisplayedOptimizedUserMessage(input, activeCellCode), type: 'openai message' });
        this.history.aiOptimizedChatHistory.push(aiOptimizedMessage);
    }
    addDebugErrorMessage(errorMessage) {
        const activeCellCode = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_0__.getActiveCellCode)(this.notebookTracker);
        const aiOptimizedPrompt = `You just ran the active code cell and received an error. Return the full code cell with the error corrected and a short explanation of the error.
        
<Reminders>

Do not: 
- Use the word "I"
- Include multiple approaches in your response
- Recreate variables that already exist

Do: 
- Use the variables that you have access to
- Keep as much of the original code as possible
- Ask for more context if you need it. 

</Reminders>

<Important Jupyter Context>

Remember that you are executing code inside a Jupyter notebook. That means you will have persistent state issues where variables from previous cells or previous code executions might still affect current code. When those errors occur, here are a few possible solutions:
1. Restarting the kernel to reset the environment if a function or variable has been unintentionally overwritten.
2. Identify which cell might need to be rerun to properly initialize the function or variable that is causing the issue.
        
For example, if an error occurs because the built-in function 'print' is overwritten by an integer, you should return the code cell with the modification to the print function removed and also return an explanation that tell the user to restart their kernel. Do not add new comments to the code cell, just return the code cell with the modification removed.
        
When a user hits an error because of a persistent state issue, tell them how to resolve it.

</Important Jupyter Context>

<Example>

Code in the active code cell:

\`\`\`python
print(y)
\`\`\`

Error Message: 
NameError: name 'y' is not defined

Output:

\`\`\`python
y = 10
print(y)
\`\`\`

The variable y has not yet been created.Define the variable y before printing it.
</Example>
        
Code in the active code cell:

\`\`\`python
${activeCellCode}
\`\`\`

Error Message: 

${errorMessage}

Output:
`;
        this.history.displayOptimizedChatHistory.push({ message: getDisplayedOptimizedUserMessage(errorMessage, activeCellCode), type: 'openai message' });
        this.history.aiOptimizedChatHistory.push({ role: 'user', content: aiOptimizedPrompt });
    }
    addExplainCodeMessage() {
        const activeCellCode = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_0__.getActiveCellCode)(this.notebookTracker);
        const aiOptimizedPrompt = `Explain the code in the active code cell to me like I have a basic understanding of Python. Don't explain each line, but instead explain the overall logic of the code.

<Example>

Code in the active code cell:

\`\`\`python
def multiply(x, y):
    return x * y
\`\`\`

Output:

This code creates a function called \`multiply\` that takes two arguments \`x\` and \`y\`, and returns the product of \`x\` and \`y\`.

</Example>

Code in the active code cell:

\`\`\`python
${activeCellCode}
\`\`\`

Output: 
`;
        this.history.displayOptimizedChatHistory.push({ message: getDisplayedOptimizedUserMessage('Explain this code', activeCellCode), type: 'openai message' });
        this.history.aiOptimizedChatHistory.push({ role: 'user', content: aiOptimizedPrompt });
    }
    addAIMessageFromResponse(message, mitoAIConnectionError = false) {
        if (message.content === null) {
            return;
        }
        const aiMessage = {
            role: 'assistant',
            content: message.content
        };
        this._addAIMessage(aiMessage, mitoAIConnectionError);
    }
    addAIMessageFromMessageContent(message, mitoAIConnectionError = false) {
        const aiMessage = {
            role: 'assistant',
            content: message
        };
        this._addAIMessage(aiMessage, mitoAIConnectionError);
    }
    _addAIMessage(aiMessage, mitoAIConnectionError = false) {
        this.history.displayOptimizedChatHistory.push({ message: aiMessage, type: mitoAIConnectionError ? 'connection error' : 'openai message' });
        this.history.aiOptimizedChatHistory.push(aiMessage);
    }
    addSystemMessage(message) {
        const systemMessage = {
            role: 'system',
            content: message
        };
        this.history.displayOptimizedChatHistory.push({ message: systemMessage, type: 'openai message' });
        this.history.aiOptimizedChatHistory.push(systemMessage);
    }
}
const getDisplayedOptimizedUserMessage = (input, activeCellCode) => {
    return {
        role: 'user',
        content: `\`\`\`python
${activeCellCode}
\`\`\`

${input}`
    };
};


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatMessage/ChatMessage.js":
/*!**********************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatMessage/ChatMessage.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_classNames__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../utils/classNames */ "./lib/utils/classNames.js");
/* harmony import */ var _CodeBlock__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./CodeBlock */ "./lib/Extensions/AiChat/ChatMessage/CodeBlock.js");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _icons_ErrorIcon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../icons/ErrorIcon */ "./lib/icons/ErrorIcon.js");





const ChatMessage = ({ message, messageIndex, mitoAIConnectionError, notebookTracker, rendermime, app, isLastAiMessage, operatingSystem, setDisplayCodeDiff, acceptAICode, rejectAICode }) => {
    if (message.role !== 'user' && message.role !== 'assistant') {
        // Filter out other types of messages, like system messages
        return null;
    }
    const messageContentParts = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_1__.splitStringWithCodeBlocks)(message);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: (0,_utils_classNames__WEBPACK_IMPORTED_MODULE_2__.classNames)("message", { "message-user": message.role === 'user' }, { 'message-assistant': message.role === 'assistant' }) }, messageContentParts.map(messagePart => {
        if (messagePart.startsWith(_utils_strings__WEBPACK_IMPORTED_MODULE_1__.PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE)) {
            // Make sure that there is actually code in the message. 
            // An empty code will look like this '```python  ```'
            // TODO: Add a test for this since its broke a few times now.
            if (messagePart.length > 14) {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CodeBlock__WEBPACK_IMPORTED_MODULE_3__["default"], { code: messagePart, role: message.role, rendermime: rendermime, notebookTracker: notebookTracker, app: app, isLastAiMessage: isLastAiMessage, operatingSystem: operatingSystem, setDisplayCodeDiff: setDisplayCodeDiff, acceptAICode: acceptAICode, rejectAICode: rejectAICode }));
            }
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                mitoAIConnectionError && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { marginRight: '4px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_ErrorIcon__WEBPACK_IMPORTED_MODULE_4__["default"], null)),
                messagePart));
        }
    })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ChatMessage);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatMessage/CodeBlock.js":
/*!********************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatMessage/CodeBlock.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _PythonCode__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./PythonCode */ "./lib/Extensions/AiChat/ChatMessage/PythonCode.js");
/* harmony import */ var _utils_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../utils/notebook */ "./lib/utils/notebook.js");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _style_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../style/CodeMessagePart.css */ "./style/CodeMessagePart.css");





const CodeBlock = ({ code, role, rendermime, notebookTracker, app, isLastAiMessage, operatingSystem, setDisplayCodeDiff, acceptAICode, rejectAICode }) => {
    const notebookName = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_2__.getNotebookName)(notebookTracker);
    const copyCodeToClipboard = () => {
        const codeWithoutMarkdown = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_3__.removeMarkdownCodeFormatting)(code);
        navigator.clipboard.writeText(codeWithoutMarkdown);
    };
    if (role === 'user') {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-container' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_PythonCode__WEBPACK_IMPORTED_MODULE_4__["default"], { code: code, rendermime: rendermime })));
    }
    if (role === 'assistant') {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-container' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-toolbar' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-location' }, notebookName),
                isLastAiMessage && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => { acceptAICode(); } },
                        "Apply ",
                        operatingSystem === 'mac' ? 'CMD+Y' : 'CTRL+Y'),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => { rejectAICode(); } },
                        "Deny ",
                        operatingSystem === 'mac' ? 'CMD+D' : 'CTRL+D'))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: copyCodeToClipboard }, "Copy")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_PythonCode__WEBPACK_IMPORTED_MODULE_4__["default"], { code: code, rendermime: rendermime })));
    }
    return react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CodeBlock);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatMessage/PythonCode.js":
/*!*********************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatMessage/PythonCode.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _style_PythonCode_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../style/PythonCode.css */ "./style/PythonCode.css");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../utils/strings */ "./lib/utils/strings.js");




const PythonCode = ({ code, rendermime }) => {
    const [node, setNode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({
            data: { ['text/markdown']: (0,_utils_strings__WEBPACK_IMPORTED_MODULE_3__.addMarkdownCodeFormatting)(code, true) },
        });
        const renderer = rendermime.createRenderer('text/markdown');
        renderer.renderModel(model);
        const node = renderer.node;
        setNode(node);
    }, [code, rendermime]); // Add dependencies to useEffect
    if (node) {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-python-code', ref: (el) => el && el.appendChild(node) });
    }
    else {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-python-code' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PythonCode);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatTaskpane.js":
/*!***********************************************!*\
  !*** ./lib/Extensions/AiChat/ChatTaskpane.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../style/ChatTaskpane.css */ "./style/ChatTaskpane.css");
/* harmony import */ var _utils_classNames__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ../../utils/classNames */ "./lib/utils/classNames.js");
/* harmony import */ var _utils_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../utils/notebook */ "./lib/utils/notebook.js");
/* harmony import */ var _ChatMessage_ChatMessage__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./ChatMessage/ChatMessage */ "./lib/Extensions/AiChat/ChatMessage/ChatMessage.js");
/* harmony import */ var _ChatHistoryManager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ChatHistoryManager */ "./lib/Extensions/AiChat/ChatHistoryManager.js");
/* harmony import */ var _utils_handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../utils/handler */ "./lib/utils/handler.js");
/* harmony import */ var _components_LoadingDots__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../../components/LoadingDots */ "./lib/components/LoadingDots.js");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");
/* harmony import */ var _icons_ResetIcon__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../icons/ResetIcon */ "./lib/icons/ResetIcon.js");
/* harmony import */ var _components_IconButton__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../components/IconButton */ "./lib/components/IconButton.js");
/* harmony import */ var _utils_codeDiff__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../utils/codeDiff */ "./lib/utils/codeDiff.js");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @codemirror/state */ "webpack/sharing/consume/default/@codemirror/state");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_codemirror_state__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _CodeDiffDisplay__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./CodeDiffDisplay */ "./lib/Extensions/AiChat/CodeDiffDisplay.js");
/* harmony import */ var _icons_SupportIcon__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../icons/SupportIcon */ "./lib/icons/SupportIcon.js");
















const getDefaultChatHistoryManager = (notebookTracker, variableManager) => {
    const chatHistoryManager = new _ChatHistoryManager__WEBPACK_IMPORTED_MODULE_3__.ChatHistoryManager(variableManager, notebookTracker);
    chatHistoryManager.addSystemMessage('You are an expert Python programmer.');
    return chatHistoryManager;
};
const ChatTaskpane = ({ notebookTracker, rendermime, variableManager, app, operatingSystem }) => {
    const textareaRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [input, setInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [chatHistoryManager, setChatHistoryManager] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(() => getDefaultChatHistoryManager(notebookTracker, variableManager));
    const chatHistoryManagerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(chatHistoryManager);
    const [loadingAIResponse, setLoadingAIResponse] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [unifiedDiffLines, setUnifiedDiffLines] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(undefined);
    const originalCodeBeforeDiff = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(undefined);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        /*
            Why we use a ref (chatHistoryManagerRef) instead of directly accessing the state (chatHistoryManager):

            The reason we use a ref here is because the function `applyLatestCode` is registered once
            when the component mounts via `app.commands.addCommand`. If we directly used `chatHistoryManager`
            in the command's execute function, it would "freeze" the state at the time of the registration
            and wouldn't update as the state changes over time.

            React's state (`useState`) is asynchronous, and the registered command won't automatically pick up the
            updated state unless the command is re-registered every time the state changes, which would require
            unregistering and re-registering the command, causing unnecessary complexity.

            By using a ref (`chatHistoryManagerRef`), we are able to keep a persistent reference to the
            latest version of `chatHistoryManager`, which is updated in this effect whenever the state
            changes. This allows us to always access the most recent state of `chatHistoryManager` in the
            `applyLatestCode` function, without needing to re-register the command or cause unnecessary re-renders.

            We still use `useState` for `chatHistoryManager` so that we can trigger a re-render of the chat
            when the state changes.
        */
        chatHistoryManagerRef.current = chatHistoryManager;
    }, [chatHistoryManager]);
    // TextAreas cannot automatically adjust their height based on the content that they contain, 
    // so instead we re-adjust the height as the content changes here. 
    const adjustHeight = () => {
        const textarea = textareaRef.current;
        if (!textarea) {
            return;
        }
        textarea.style.minHeight = 'auto';
        // The height should be 20 at minimum to support the placeholder
        const minHeight = textarea.scrollHeight < 20 ? 20 : textarea.scrollHeight;
        textarea.style.minHeight = `${minHeight}px`;
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        adjustHeight();
    }, [input]);
    const getDuplicateChatHistoryManager = () => {
        /*
            We use getDuplicateChatHistoryManager() instead of directly accessing the state variable because
            the COMMAND_MITO_AI_SEND_MESSAGE is registered in a useEffect on initial render, which
            would otherwise always use the initial state values. By using a function, we ensure we always
            get the most recent chat history, even when the command is executed later.
        */
        return chatHistoryManagerRef.current.createDuplicateChatHistoryManager();
    };
    /*
        Send a message with a specific input, clearing what is currently in the chat input.
        This is useful when we want to send the error message from the MIME renderer directly
        to the AI chat.
    */
    const sendDebugErrorMessage = async (errorMessage) => {
        // Step 1: Add the user's message to the chat history
        const newChatHistoryManager = getDuplicateChatHistoryManager();
        newChatHistoryManager.addDebugErrorMessage(errorMessage);
        // Step 2: Send the message to the AI
        const aiMessage = await _sendMessageToOpenAI(newChatHistoryManager);
        // Step 3: Update the code diff stripes
        updateCodeDiffStripes(aiMessage);
    };
    const sendExplainCodeMessage = () => {
        // Step 1: Add the user's message to the chat history
        const newChatHistoryManager = getDuplicateChatHistoryManager();
        newChatHistoryManager.addExplainCodeMessage();
        // Step 2: Send the message to the AI
        _sendMessageToOpenAI(newChatHistoryManager);
        // Step 3: No post processing step needed for explaining code. 
    };
    /*
        Send whatever message is currently in the chat input
    */
    const sendChatInputMessage = async () => {
        // Step 1: Add the user's message to the chat history
        const newChatHistoryManager = getDuplicateChatHistoryManager();
        newChatHistoryManager.addChatInputMessage(input);
        // Step 2: Send the message to the AI
        const aiMessage = await _sendMessageToOpenAI(newChatHistoryManager);
        // Step 3: Update the code diff stripes
        updateCodeDiffStripes(aiMessage);
    };
    const _sendMessageToOpenAI = async (newChatHistoryManager) => {
        setInput('');
        setLoadingAIResponse(true);
        let aiRespone = undefined;
        try {
            const apiResponse = await (0,_utils_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('mito_ai/completion', {
                method: 'POST',
                body: JSON.stringify({
                    messages: newChatHistoryManager.getAIOptimizedHistory()
                })
            });
            if (apiResponse.type === 'success') {
                const response = apiResponse.response;
                const aiMessage = response.choices[0].message;
                newChatHistoryManager.addAIMessageFromResponse(aiMessage);
                setChatHistoryManager(newChatHistoryManager);
                aiRespone = aiMessage;
            }
            else {
                newChatHistoryManager.addAIMessageFromMessageContent(apiResponse.errorMessage, true);
                setChatHistoryManager(newChatHistoryManager);
            }
        }
        catch (error) {
            console.error('Error calling OpenAI API:', error);
        }
        finally {
            setLoadingAIResponse(false);
            return aiRespone;
        }
    };
    const updateCodeDiffStripes = (aiMessage) => {
        if (!aiMessage) {
            return;
        }
        const activeCellCode = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_5__.getActiveCellCode)(notebookTracker);
        // Extract the code from the AI's message and then calculate the code diffs
        const aiGeneratedCode = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_6__.getCodeBlockFromMessage)(aiMessage);
        const aiGeneratedCodeCleaned = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_6__.removeMarkdownCodeFormatting)(aiGeneratedCode || '');
        const { unifiedCodeString, unifiedDiffs } = (0,_utils_codeDiff__WEBPACK_IMPORTED_MODULE_7__.getCodeDiffsAndUnifiedCodeString)(activeCellCode, aiGeneratedCodeCleaned);
        // Store the original code so that we can revert to it if the user rejects the AI's code
        originalCodeBeforeDiff.current = activeCellCode || '';
        // Temporarily write the unified code string to the active cell so we can display
        // the code diffs to the user. Once the user accepts or rejects the code, we'll 
        // apply the correct version of the code.
        (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_5__.writeCodeToActiveCell)(notebookTracker, unifiedCodeString);
        setUnifiedDiffLines(unifiedDiffs);
    };
    const displayOptimizedChatHistory = chatHistoryManager.getDisplayOptimizedHistory();
    const acceptAICode = () => {
        const latestChatHistoryManager = chatHistoryManagerRef.current;
        const lastAIMessage = latestChatHistoryManager.getLastAIMessage();
        if (!lastAIMessage) {
            return;
        }
        const aiGeneratedCode = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_6__.getCodeBlockFromMessage)(lastAIMessage.message);
        if (!aiGeneratedCode) {
            return;
        }
        _applyCode(aiGeneratedCode);
    };
    const rejectAICode = () => {
        const originalDiffedCode = originalCodeBeforeDiff.current;
        if (originalDiffedCode === undefined) {
            return;
        }
        _applyCode(originalDiffedCode);
    };
    const _applyCode = (code) => {
        (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_5__.writeCodeToActiveCell)(notebookTracker, code, true);
        setUnifiedDiffLines(undefined);
        originalCodeBeforeDiff.current = undefined;
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        /*
            Add a new command to the JupyterLab command registry that applies the latest AI generated code
            to the active code cell. Do this inside of the useEffect so that we only register the command
            the first time we create the chat. Registering the command when it is already created causes
            errors.
        */
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_8__.COMMAND_MITO_AI_APPLY_LATEST_CODE, {
            execute: () => {
                acceptAICode();
            }
        });
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_8__.COMMAND_MITO_AI_REJECT_LATEST_CODE, {
            execute: () => {
                rejectAICode();
            }
        });
        app.commands.addKeyBinding({
            command: _commands__WEBPACK_IMPORTED_MODULE_8__.COMMAND_MITO_AI_APPLY_LATEST_CODE,
            keys: ['Accel Y'],
            selector: 'body',
        });
        app.commands.addKeyBinding({
            command: _commands__WEBPACK_IMPORTED_MODULE_8__.COMMAND_MITO_AI_REJECT_LATEST_CODE,
            keys: ['Accel D'],
            selector: 'body',
        });
        /*
            Add a new command to the JupyterLab command registry that sends the current chat message.
            We use this to automatically send the message when the user adds an error to the chat.
        */
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_8__.COMMAND_MITO_AI_SEND_DEBUG_ERROR_MESSAGE, {
            execute: (args) => {
                if (args === null || args === void 0 ? void 0 : args.input) {
                    sendDebugErrorMessage(args.input.toString());
                }
            }
        });
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_8__.COMMAND_MITO_AI_SEND_EXPLAIN_CODE_MESSAGE, {
            execute: () => {
                sendExplainCodeMessage();
            }
        });
    }, []);
    // Create a WeakMap to store compartments per code cell
    const codeDiffStripesCompartments = react__WEBPACK_IMPORTED_MODULE_0___default().useRef(new WeakMap());
    // Function to update the extensions of code cells
    const updateCodeCellsExtensions = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        var _a;
        const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (!notebook) {
            return;
        }
        const activeCellIndex = notebook.activeCellIndex;
        notebook.widgets.forEach((cell, index) => {
            if (cell.model.type === 'code') {
                const isActiveCodeCell = activeCellIndex === index;
                const codeCell = cell;
                const cmEditor = codeCell.editor;
                const editorView = cmEditor === null || cmEditor === void 0 ? void 0 : cmEditor.editor;
                if (editorView) {
                    let compartment = codeDiffStripesCompartments.current.get(codeCell);
                    if (!compartment) {
                        // Create a new compartment and store it
                        compartment = new _codemirror_state__WEBPACK_IMPORTED_MODULE_2__.Compartment();
                        codeDiffStripesCompartments.current.set(codeCell, compartment);
                        // Apply the initial configuration
                        editorView.dispatch({
                            effects: _codemirror_state__WEBPACK_IMPORTED_MODULE_2__.StateEffect.appendConfig.of(compartment.of(unifiedDiffLines !== undefined && isActiveCodeCell ? (0,_CodeDiffDisplay__WEBPACK_IMPORTED_MODULE_9__.codeDiffStripesExtension)({ unifiedDiffLines: unifiedDiffLines }) : [])),
                        });
                    }
                    else {
                        // Reconfigure the compartment
                        editorView.dispatch({
                            effects: compartment.reconfigure(unifiedDiffLines !== undefined && isActiveCodeCell ? (0,_CodeDiffDisplay__WEBPACK_IMPORTED_MODULE_9__.codeDiffStripesExtension)({ unifiedDiffLines: unifiedDiffLines }) : []),
                        });
                    }
                }
                else {
                    console.log('Mito AI: editor view not found when applying code diff stripes');
                }
            }
        });
    }, [unifiedDiffLines, notebookTracker]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        updateCodeCellsExtensions();
    }, [unifiedDiffLines, updateCodeCellsExtensions]);
    const lastAIMessagesIndex = chatHistoryManager.getLastAIMessageIndex();
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-taskpane" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-taskpane-header" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_IconButton__WEBPACK_IMPORTED_MODULE_10__["default"], { icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_SupportIcon__WEBPACK_IMPORTED_MODULE_11__["default"], null), title: "Get Help", onClick: () => {
                    window.open('mailto:founders@sagacollab.com?subject=Mito AI Chat Support', '_blank');
                } }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_IconButton__WEBPACK_IMPORTED_MODULE_10__["default"], { icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_ResetIcon__WEBPACK_IMPORTED_MODULE_12__["default"], null), title: "Clear the chat history", onClick: () => {
                    setChatHistoryManager(getDefaultChatHistoryManager(notebookTracker, variableManager));
                } })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-messages" }, displayOptimizedChatHistory.map((displayOptimizedChat, index) => {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ChatMessage_ChatMessage__WEBPACK_IMPORTED_MODULE_13__["default"], { message: displayOptimizedChat.message, mitoAIConnectionError: displayOptimizedChat.type === 'connection error', messageIndex: index, notebookTracker: notebookTracker, rendermime: rendermime, app: app, isLastAiMessage: index === lastAIMessagesIndex, operatingSystem: operatingSystem, setDisplayCodeDiff: setUnifiedDiffLines, acceptAICode: acceptAICode, rejectAICode: rejectAICode }));
        }).filter(message => message !== null)),
        loadingAIResponse &&
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-loading-message" },
                "Loading AI Response ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_LoadingDots__WEBPACK_IMPORTED_MODULE_14__["default"], null)),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("textarea", { ref: textareaRef, className: (0,_utils_classNames__WEBPACK_IMPORTED_MODULE_15__.classNames)("message", "message-user", 'chat-input'), placeholder: displayOptimizedChatHistory.length < 2 ? "Ask your personal Python expert anything!" : "Follow up on the conversation", value: input, onChange: (e) => { setInput(e.target.value); }, onKeyDown: (e) => {
                // Enter key sends the message, but we still want to allow 
                // shift + enter to add a new line.
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendChatInputMessage();
                }
            } })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ChatTaskpane);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatWidget.js":
/*!*********************************************!*\
  !*** ./lib/Extensions/AiChat/ChatWidget.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   buildChatWidget: () => (/* binding */ buildChatWidget),
/* harmony export */   chatIcon: () => (/* binding */ chatIcon)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ChatTaskpane__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./ChatTaskpane */ "./lib/Extensions/AiChat/ChatTaskpane.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _src_icons_ChatIcon_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../src/icons/ChatIcon.svg */ "./src/icons/ChatIcon.svg");
/* harmony import */ var _utils_user__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../utils/user */ "./lib/utils/user.js");






const chatIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({
    name: 'mito_ai',
    svgstr: _src_icons_ChatIcon_svg__WEBPACK_IMPORTED_MODULE_3__
});
function buildChatWidget(app, notebookTracker, rendermime, variableManager) {
    // Get the operating system here so we don't have to do it each time the chat changes.
    // The operating system won't change, duh. 
    const operatingSystem = (0,_utils_user__WEBPACK_IMPORTED_MODULE_4__.getOperatingSystem)();
    const chatWidget = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ChatTaskpane__WEBPACK_IMPORTED_MODULE_5__["default"], { app: app, notebookTracker: notebookTracker, rendermime: rendermime, variableManager: variableManager, operatingSystem: operatingSystem }));
    chatWidget.id = 'mito_ai';
    chatWidget.title.icon = chatIcon;
    chatWidget.title.caption = 'AI Chat for your JupyterLab';
    return chatWidget;
}


/***/ }),

/***/ "./lib/Extensions/AiChat/CodeDiffDisplay.js":
/*!**************************************************!*\
  !*** ./lib/Extensions/AiChat/CodeDiffDisplay.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   codeDiffStripesExtension: () => (/* binding */ codeDiffStripesExtension)
/* harmony export */ });
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @codemirror/state */ "webpack/sharing/consume/default/@codemirror/state");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_codemirror_state__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @codemirror/view */ "webpack/sharing/consume/default/@codemirror/view");
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_codemirror_view__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils_arrays__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../utils/arrays */ "./lib/utils/arrays.js");



// Defines new styles for this extension
const baseTheme = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.EditorView.baseTheme({
    // We need to set some transparency because the stripes are above the selection layer
    '.cm-codeDiffRemovedStripe': { backgroundColor: 'rgba(250, 212, 212, 0.62)' },
    '.cm-codeDiffInsertedStripe': { backgroundColor: 'rgba(79, 255, 105, 0.38)' },
});
// Resolve step to use in the editor
const unifiedDiffLines = _codemirror_state__WEBPACK_IMPORTED_MODULE_0__.Facet.define({
    combine: (unifiedDiffLines) => {
        return unifiedDiffLines;
    }
});
// Add decoration to editor lines
const removedStripe = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.Decoration.line({
    attributes: { class: 'cm-codeDiffRemovedStripe' }
});
const insertedStripe = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.Decoration.line({
    attributes: { class: 'cm-codeDiffInsertedStripe' }
});
// Create the range of lines requiring decorations
const getCodeDiffStripesDecoration = (view) => {
    const unifiedDiffLinesFacet = view.state.facet(unifiedDiffLines)[0];
    const builder = new _codemirror_state__WEBPACK_IMPORTED_MODULE_0__.RangeSetBuilder();
    for (const { from, to } of view.visibleRanges) {
        for (let pos = from; pos <= to;) {
            const line = view.state.doc.lineAt(pos);
            // console.log('unifiedDiffLinesFacet[line.number - 1]', unifiedDiffLinesFacet[line.number - 1])
            // console.log('line', line.number)
            // The code mirror line numbers are 1-indexed, but our diff lines are 0-indexed
            if (line.number - 1 >= unifiedDiffLinesFacet.length) {
                /*
                  Because we need to rerender the decorations each time the doc changes or viewport updates
                  (maybe we don't need to, but the code mirror examples does this so we will to for now) there
                  is a race condition where sometimes the content of the code cell updates before the unified diff lines
                  are updated. As a result, we need to break out of the loop before we get a null pointer error.
        
                  This isn't a problem because right afterwards, the code mirror updates again due to the unified diff lines
                  being updated. In that render, we get the correct results.
                */
                break;
            }
            if (unifiedDiffLinesFacet[line.number - 1].type === 'removed') {
                builder.add(line.from, line.from, removedStripe);
            }
            if (unifiedDiffLinesFacet[line.number - 1].type === 'inserted') {
                builder.add(line.from, line.from, insertedStripe);
            }
            pos = line.to + 1;
        }
    }
    return builder.finish();
};
// Update the decoration status of the editor view
const showStripes = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.ViewPlugin.fromClass(class {
    constructor(view) {
        this.decorations = getCodeDiffStripesDecoration(view);
    }
    update(update) {
        const oldUnifiedDiffLines = update.startState.facet(unifiedDiffLines);
        const newUnifiedDiffLines = update.view.state.facet(unifiedDiffLines);
        if (update.docChanged ||
            update.viewportChanged ||
            !(0,_utils_arrays__WEBPACK_IMPORTED_MODULE_2__.deepEqualArrays)(oldUnifiedDiffLines[0], newUnifiedDiffLines[0])) {
            this.decorations = getCodeDiffStripesDecoration(update.view);
        }
    }
}, {
    decorations: v => v.decorations
});
// Create the Code Mirror Extension to apply the code diff stripes to the code mirror editor
function codeDiffStripesExtension(options = {}) {
    return [
        baseTheme,
        options.unifiedDiffLines ? unifiedDiffLines.of(options.unifiedDiffLines) : [],
        showStripes
    ];
}


/***/ }),

/***/ "./lib/Extensions/CellToolbarButtons/CellToolbarButtonsPlugin.js":
/*!***********************************************************************!*\
  !*** ./lib/Extensions/CellToolbarButtons/CellToolbarButtonsPlugin.js ***!
  \***********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   lightBulbIcon: () => (/* binding */ lightBulbIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _src_icons_LightbulbIcon_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../src/icons/LightbulbIcon.svg */ "./src/icons/LightbulbIcon.svg");




const lightBulbIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: 'lightbulb-icon',
    svgstr: _src_icons_LightbulbIcon_svg__WEBPACK_IMPORTED_MODULE_2__
});
const CellToolbarButtonsPlugin = {
    // Important: The Cell Toolbar Buttons are added to the toolbar registry via the schema/plugin.json file.
    // The id here must be mito-ai:plugin otherwise the buttons are not successfull added. My understanding is that
    // the id must match the name of the package and `plugin` must be used when working with the schema/plugin.json file.
    id: 'mito-ai:plugin',
    description: 'Adds an "explain code cell with AI" button to the cell toolbar',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        const { commands } = app;
        // Important: To add a button to the cell toolbar, the command must start with "toolbar-button:"
        // and the command must match the command in the schema/plugin.json file.
        commands.addCommand('toolbar-button:explain-code', {
            icon: lightBulbIcon,
            caption: 'Explain code in AI Chat',
            execute: () => {
                /*
                    In order to click on the cell toolbar button, that cell must be the active cell,
                    so the ChatHistoryManager will take care of providing the cell context.
                */
                app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_3__.COMMAND_MITO_AI_OPEN_CHAT);
                app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_3__.COMMAND_MITO_AI_SEND_EXPLAIN_CODE_MESSAGE);
            },
            isVisible: () => { var _a; return ((_a = notebookTracker.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code' && app.commands.hasCommand(_commands__WEBPACK_IMPORTED_MODULE_3__.COMMAND_MITO_AI_SEND_EXPLAIN_CODE_MESSAGE); }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CellToolbarButtonsPlugin);


/***/ }),

/***/ "./lib/Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin.js":
/*!*********************************************************************!*\
  !*** ./lib/Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin.js ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");
/* harmony import */ var _icons_MagicWand__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../icons/MagicWand */ "./lib/icons/MagicWand.js");
/* harmony import */ var _style_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../style/ErrorMimeRendererPlugin.css */ "./style/ErrorMimeRendererPlugin.css");







const ErrorMessage = ({ onDebugClick }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "error-mime-renderer-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: onDebugClick, className: 'error-mime-renderer-button' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_MagicWand__WEBPACK_IMPORTED_MODULE_5__["default"], null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Fix Error in AI Chat"))));
};
/**
 * A mime renderer plugin for the mimetype application/vnd.jupyter.stderr
 *
 * This plugin augments the standard error output with a prompt to debug the error in the chat interface.
*/
const ErrorMimeRendererPlugin = {
    id: 'mito-ai:debug-error-with-ai',
    autoStart: true,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry],
    activate: (app, rendermime) => {
        const factory = rendermime.getFactory('application/vnd.jupyter.stderr');
        if (factory) {
            rendermime.addFactory({
                safe: true,
                mimeTypes: ['application/vnd.jupyter.stderr'],
                createRenderer: (options) => {
                    const originalRenderer = factory.createRenderer(options);
                    return new AugmentedStderrRenderer(app, originalRenderer);
                }
            }, -1); // Giving this renderer a lower rank than the default renderer gives this default priority
        }
    }
};
/**
 * A widget that extends the default StderrRenderer.
*/
class AugmentedStderrRenderer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(app, originalRenderer) {
        super();
        this.app = app;
        this.originalRenderer = originalRenderer;
    }
    /**
     * Render the original error message and append the custom prompt.
     */
    async renderModel(model) {
        const resolveInChatDiv = document.createElement('div');
        react_dom__WEBPACK_IMPORTED_MODULE_1___default().render(react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ErrorMessage, { onDebugClick: () => this.openChatInterfaceWithError(model) }), resolveInChatDiv);
        this.node.appendChild(resolveInChatDiv);
        // Get the original renderer and append it to the output
        await this.originalRenderer.renderModel(model);
        this.node.appendChild(this.originalRenderer.node);
    }
    /*
        Open the chat interface and preload the error message into
        the user input.
    */
    openChatInterfaceWithError(model) {
        const conciseErrorMessage = this.getErrorString(model);
        this.app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT);
        this.app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_SEND_DEBUG_ERROR_MESSAGE, { input: conciseErrorMessage });
    }
    /*
        Get the error string from the model.
    */
    getErrorString(model) {
        const error = model.data['application/vnd.jupyter.error'];
        if (error && typeof error === 'object' && 'ename' in error && 'evalue' in error) {
            return `${error.ename}: ${error.evalue}`;
        }
        return '';
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ErrorMimeRendererPlugin);


/***/ }),

/***/ "./lib/Extensions/VariableManager/VariableInspector.js":
/*!*************************************************************!*\
  !*** ./lib/Extensions/VariableManager/VariableInspector.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   setupKernelListener: () => (/* binding */ setupKernelListener)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);

// TODO: Use something like raw-loader to load an actual python file 
// to make it easier to modify the script without creating syntax errors.
const pythonVariableInspectionScript = `import json


# We need to check if pandas is imported so we know if its safe
# to check for pandas dataframes 
_is_pandas_imported = False
try:
    import pandas as pd
    _is_pandas_imported = True
except:
    pass

# Function to convert dataframe to structured format
def get_dataframe_structure(df, sample_size=5):
    structure = {}
    for column in df.columns:
        structure[column] = {
            "dtype": str(df[column].dtype),
            "samples": df[column].head(sample_size).tolist()
        }
    return structure

def structured_globals():
    output = []
    for k, v in globals().items():
        if not k.startswith("_") and k not in ("In", "Out", "json") and not callable(v):
            if _is_pandas_imported and isinstance(v, pd.DataFrame):
                output.append({
                    "variable_name": k,
                    "type": "pd.DataFrame",
                    "value": get_dataframe_structure(v)
                })
            else:
                output.append({
                    "variable_name": k,
                    "type": str(type(v)),
                    "value": repr(v)
                })

    return json.dumps(output)

print(structured_globals())
`;
// Function to fetch variables and sync with the frontend
async function fetchVariablesAndUpdateState(notebookPanel, setVariables) {
    var _a;
    const kernel = (_a = notebookPanel.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (kernel) {
        // Request the kernel to execute a command to fetch global variables
        const future = kernel.requestExecute({
            code: pythonVariableInspectionScript,
            // Adding silent: true prevents a execute_input message from being sent. This is important 
            // because it prevents an infinite loop where we fetch variables and in the process trigger 
            // a new execute_input which leads to fetching variables again.
            silent: true
        });
        // Listen for the output from the kernel
        future.onIOPub = (msg) => {
            // A 'stream' message represents standard output (stdout) or standard error (stderr) produced 
            // during the execution of code in the kernel.
            if (_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.isStreamMsg(msg)) {
                if (msg.content.name === 'stdout') {
                    try {
                        setVariables(JSON.parse(msg.content.text));
                    }
                    catch (e) {
                        console.log("Error parsing variables", e);
                    }
                }
            }
        };
    }
}
// Setup kernel execution listener
function setupKernelListener(notebookTracker, setVariables) {
    notebookTracker.currentChanged.connect((tracker, notebookPanel) => {
        if (!notebookPanel) {
            return;
        }
        // Listen to kernel messages
        notebookPanel.context.sessionContext.iopubMessage.connect((sender, msg) => {
            // Watch for execute_input messages, which indicate is a request to execute code. 
            // Previosuly, we watched for 'execute_result' messages, but these are only returned
            // from the kernel when a code cell prints a value to the output cell, which is not what we want.
            // TODO: Check if there is a race condition where we might end up fetching variables before the 
            // code is executed. I don't think this is the case because the kernel runs in one thread I believe.
            if (msg.header.msg_type === 'execute_input') {
                fetchVariablesAndUpdateState(notebookPanel, setVariables);
            }
        });
    });
}


/***/ }),

/***/ "./lib/Extensions/VariableManager/VariableManagerPlugin.js":
/*!*****************************************************************!*\
  !*** ./lib/Extensions/VariableManager/VariableManagerPlugin.js ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IVariableManager: () => (/* binding */ IVariableManager),
/* harmony export */   VariableManager: () => (/* binding */ VariableManager),
/* harmony export */   VariableManagerPlugin: () => (/* binding */ VariableManagerPlugin),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _VariableInspector__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./VariableInspector */ "./lib/Extensions/VariableManager/VariableInspector.js");



// The provides field in JupyterLab’s JupyterFrontEndPlugin expects a token 
// that can be used to look up the service in the dependency injection system,
// so we define a new token for the VariableManager
// TODO: Should this still be called mito-ai or something else? Do I need a new name for 
// each extension? I don't think so.
const IVariableManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('mito-ai:IVariableManager');
class VariableManager {
    constructor(notebookTracker) {
        this._variables = [];
        (0,_VariableInspector__WEBPACK_IMPORTED_MODULE_2__.setupKernelListener)(notebookTracker, this.setVariables.bind(this));
    }
    get variables() {
        return this._variables;
    }
    setVariables(newVars) {
        this._variables = newVars;
        console.log("Variables updated", this._variables);
    }
}
const VariableManagerPlugin = {
    id: 'mito-ai:variable-manager',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    provides: IVariableManager,
    activate: (app, notebookTracker) => {
        return new VariableManager(notebookTracker);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (VariableManagerPlugin);


/***/ }),

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   COMMAND_MITO_AI_APPLY_LATEST_CODE: () => (/* binding */ COMMAND_MITO_AI_APPLY_LATEST_CODE),
/* harmony export */   COMMAND_MITO_AI_OPEN_CHAT: () => (/* binding */ COMMAND_MITO_AI_OPEN_CHAT),
/* harmony export */   COMMAND_MITO_AI_REJECT_LATEST_CODE: () => (/* binding */ COMMAND_MITO_AI_REJECT_LATEST_CODE),
/* harmony export */   COMMAND_MITO_AI_SEND_DEBUG_ERROR_MESSAGE: () => (/* binding */ COMMAND_MITO_AI_SEND_DEBUG_ERROR_MESSAGE),
/* harmony export */   COMMAND_MITO_AI_SEND_EXPLAIN_CODE_MESSAGE: () => (/* binding */ COMMAND_MITO_AI_SEND_EXPLAIN_CODE_MESSAGE),
/* harmony export */   COMMAND_MITO_AI_SEND_MESSAGE: () => (/* binding */ COMMAND_MITO_AI_SEND_MESSAGE)
/* harmony export */ });
const MITO_AI = 'mito_ai';
const COMMAND_MITO_AI_OPEN_CHAT = `${MITO_AI}:open-chat`;
const COMMAND_MITO_AI_APPLY_LATEST_CODE = `${MITO_AI}:apply-latest-code`;
const COMMAND_MITO_AI_REJECT_LATEST_CODE = `${MITO_AI}:reject-latest-code`;
const COMMAND_MITO_AI_SEND_MESSAGE = `${MITO_AI}:send-message`;
const COMMAND_MITO_AI_SEND_EXPLAIN_CODE_MESSAGE = `${MITO_AI}:send-explain-code-message`;
const COMMAND_MITO_AI_SEND_DEBUG_ERROR_MESSAGE = `${MITO_AI}:send-debug-error-message`;


/***/ }),

/***/ "./lib/components/IconButton.js":
/*!**************************************!*\
  !*** ./lib/components/IconButton.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_IconButton_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/IconButton.css */ "./style/IconButton.css");


const IconButton = ({ icon, onClick, title }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "icon-button", onClick: onClick, title: title }, icon));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (IconButton);


/***/ }),

/***/ "./lib/components/LoadingDots.js":
/*!***************************************!*\
  !*** ./lib/components/LoadingDots.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Mito

/*
    Dot, dot, dots. They count, so that you can display something as loading.
*/
const LoadingDots = () => {
    // We use a count to track the number of ...s to display.
    // 0 -> '', 1 -> '.', 2 -> '..', 3 -> '...'. Wraps % 4.
    const [indicatorState, setIndicatorState] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(1);
    // Schedule a change to update the loading indicator, every .5 seconds
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const interval = setInterval(() => {
            setIndicatorState(indicatorState => indicatorState + 1);
        }, 500);
        return () => clearInterval(interval);
    }, []);
    const someNumberOfDots = '.'.repeat(indicatorState % 4);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null, someNumberOfDots));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (LoadingDots);


/***/ }),

/***/ "./lib/icons/ErrorIcon.js":
/*!********************************!*\
  !*** ./lib/icons/ErrorIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const ErrorIcon = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "12", height: "12", viewBox: "0 0 12 12", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M6.00024 12C9.31251 12 12 9.31179 12 6.00024C12 2.68797 9.31803 0 6.00024 0C2.68185 0 0 2.68821 0 6.00024C0 9.31251 2.68821 12 5.99976 12H6.00024ZM5.02816 2.53827C5.02816 2.37043 5.15995 2.23809 5.32834 2.23809H6.67209C6.83993 2.23809 6.97227 2.36988 6.97227 2.53827V6.54043C6.97227 6.70827 6.84048 6.84061 6.67209 6.84061H5.32834C5.16051 6.84061 5.02816 6.70882 5.02816 6.54043V2.53827ZM6.00024 7.81209C6.53416 7.81209 6.97232 8.25026 6.97232 8.78416C6.97232 9.31807 6.53415 9.75624 6.00024 9.75624C5.46633 9.75624 5.02816 9.31807 5.02816 8.78416C5.02816 8.25026 5.46633 7.81209 6.00024 7.81209Z", fill: "black" })));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ErrorIcon);


/***/ }),

/***/ "./lib/icons/MagicWand.js":
/*!********************************!*\
  !*** ./lib/icons/MagicWand.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const MagicWandIcon = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "16", height: "16", viewBox: "0 0 16 16", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { "clip-path": "url(#clip0_8258_341)" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M11.5174 4.48082C11.2454 4.20952 10.8057 4.20952 10.5338 4.48082L7.58203 7.43256L8.56567 8.4162L11.5166 5.46446C11.788 5.19389 11.7886 4.7528 11.5173 4.48082H11.5174Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M0.20398 15.7957C0.475953 16.0677 0.915647 16.0677 1.18762 15.7957L8.07455 8.90942L7.09091 7.92578L0.20398 14.812C-0.0679933 15.084 -0.0679933 15.5237 0.20398 15.7957Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M11.1299 1.39133L10.7821 0L10.4343 1.39133L9.04297 1.73915L10.4343 2.08701L10.7821 3.47835L11.1299 2.08701L12.5213 1.73915L11.1299 1.39133Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M14.2607 3.47656L13.9128 4.8679L12.5215 5.21571L13.9128 5.56352L14.2607 6.95486L14.6085 5.56352L15.9998 5.21571L14.6085 4.8679L14.2607 3.47656Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M12.5213 7.65234L11.8256 10.435L9.04297 11.1306L11.8256 11.8263L12.5213 14.609L13.2169 11.8263L15.9996 11.1306L13.2169 10.435L12.5213 7.65234Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M6.26186 4.17397L9.04453 3.47835L6.26186 2.78267L5.56618 0L4.87056 2.78267L2.08789 3.47835L4.87056 4.17397L5.56618 6.95664L6.26186 4.17397Z", fill: "white" })),
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("defs", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("clipPath", { id: "clip0_8258_341" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("rect", { width: "16", height: "16", fill: "white" })))));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MagicWandIcon);


/***/ }),

/***/ "./lib/icons/ResetIcon.js":
/*!********************************!*\
  !*** ./lib/icons/ResetIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const ResetIcon = () => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "16", height: "16", viewBox: "0 0 16 16", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { "fill-rule": "evenodd", "clip-rule": "evenodd", d: "M3.83835 4.66666C4.80966 3.455 6.29889 2.6764 7.97035 2.6668C7.99332 2.66664 8.01619 2.66664 8.0391 2.6668C9.4619 2.67654 10.7524 3.24336 11.7031 4.16C11.7583 4.21317 11.8123 4.26755 11.8652 4.32312C12.7592 5.26218 13.3145 6.52685 13.3346 7.92098C13.3355 7.97619 13.3355 8.0314 13.3346 8.08666C13.3126 9.46933 12.7643 10.7241 11.8815 11.6597C11.811 11.7345 11.7383 11.8072 11.6634 11.8779C10.7263 12.763 9.46861 13.3122 8.08288 13.3327C8.03173 13.3335 7.98048 13.3335 7.92924 13.3329C5.2419 13.2969 3.0343 11.2734 2.70977 8.66526C2.6643 8.29995 2.37018 7.99995 2.00201 7.99995C1.63384 7.99995 1.3319 8.29917 1.36862 8.66547C1.39118 8.89026 1.42508 9.11313 1.47003 9.33329C1.70634 10.4909 2.24795 11.5734 3.04976 12.463C4.15336 13.6876 5.6715 14.46 7.3111 14.6306C8.9507 14.8015 10.5954 14.3588 11.9278 13.3881C13.2602 12.4173 14.1856 10.9874 14.5255 9.37434C14.8653 7.76127 14.5955 6.07954 13.768 4.65367C12.9406 3.22794 11.6143 2.15914 10.0452 1.65394C8.47618 1.14867 6.77538 1.24274 5.27151 1.91795C4.23416 2.38369 3.34124 3.10317 2.66871 3.99982V2.66649C2.66871 2.29831 2.37022 1.99982 2.00204 1.99982C1.63387 1.99982 1.33538 2.29831 1.33538 2.66649V5.99982H4.66871C5.03688 5.99982 5.33538 5.70133 5.33538 5.33315C5.33538 4.96498 5.03688 4.66649 4.66871 4.66649L3.83835 4.66666Z", fill: "black" })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ResetIcon);


/***/ }),

/***/ "./lib/icons/SupportIcon.js":
/*!**********************************!*\
  !*** ./lib/icons/SupportIcon.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const SupportIcon = () => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "15", height: "16", viewBox: "0 0 15 16", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M12.4445 5.35708V5.33338C12.4445 3.90818 11.8904 2.56889 10.883 1.56148C9.87562 0.553941 8.53635 0 7.11113 0C4.16886 0 1.77778 2.39108 1.77778 5.33334V5.35705C0.773343 5.50223 0 6.36446 0 7.40726V9.77764C0 10.9213 0.930372 11.8519 2.07424 11.8519H2.66683C3.15573 11.8519 3.55572 11.4519 3.55572 10.963V6.22223C3.55572 5.73334 3.15573 5.33334 2.66683 5.33334H2.37053C2.37053 2.72008 4.49802 0.592594 7.11128 0.592594C8.37646 0.592594 9.56763 1.08445 10.4624 1.98223C11.3572 2.88001 11.852 4.06816 11.852 5.33331H11.5557C11.0668 5.33331 10.6668 5.73331 10.6668 6.2222V10.963C10.6668 11.4519 11.0668 11.8518 11.5557 11.8518H11.852V13.037C11.852 13.8548 11.1883 14.5185 10.3705 14.5185H8.84755C8.71422 14.0089 8.25496 13.6296 7.70385 13.6296H6.51866C5.86383 13.6296 5.33347 14.16 5.33347 14.8148C5.33347 15.4696 5.86383 16 6.51866 16H7.70385C8.25496 16 8.71423 15.6207 8.84755 15.1111H10.3705C11.5142 15.1111 12.4448 14.1807 12.4448 13.0369V11.828C13.4492 11.6828 14.2225 10.8206 14.2225 9.77777V7.40739C14.2225 6.36443 13.4492 5.50224 12.4448 5.35717L12.4445 5.35708Z", fill: "black" })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SupportIcon);


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Extensions_AiChat_AiChatPlugin__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Extensions/AiChat/AiChatPlugin */ "./lib/Extensions/AiChat/AiChatPlugin.js");
/* harmony import */ var _Extensions_VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Extensions/VariableManager/VariableManagerPlugin */ "./lib/Extensions/VariableManager/VariableManagerPlugin.js");
/* harmony import */ var _Extensions_ErrorMimeRenderer_ErrorMimeRendererPlugin__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin */ "./lib/Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin.js");
/* harmony import */ var _Extensions_CellToolbarButtons_CellToolbarButtonsPlugin__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Extensions/CellToolbarButtons/CellToolbarButtonsPlugin */ "./lib/Extensions/CellToolbarButtons/CellToolbarButtonsPlugin.js");




// This is the main entry point to the mito-ai extension. It must export all of the top level 
// extensions that we want to load.
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    _Extensions_AiChat_AiChatPlugin__WEBPACK_IMPORTED_MODULE_0__["default"],
    _Extensions_ErrorMimeRenderer_ErrorMimeRendererPlugin__WEBPACK_IMPORTED_MODULE_1__["default"],
    _Extensions_VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_2__["default"],
    _Extensions_CellToolbarButtons_CellToolbarButtonsPlugin__WEBPACK_IMPORTED_MODULE_3__["default"]
]);


/***/ }),

/***/ "./lib/utils/arrays.js":
/*!*****************************!*\
  !*** ./lib/utils/arrays.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   deepEqualArrays: () => (/* binding */ deepEqualArrays)
/* harmony export */ });
const deepEqualArrays = (arr1, arr2) => {
    if (arr1.length !== arr2.length)
        return false;
    for (let i = 0; i < arr1.length; i++) {
        if (typeof arr1[i] === 'object' && typeof arr2[i] === 'object') {
            if (!deepEqualArrays(arr1[i], arr2[i]))
                return false;
        }
        else if (arr1[i] !== arr2[i]) {
            return false;
        }
    }
    return true;
};


/***/ }),

/***/ "./lib/utils/classNames.js":
/*!*********************************!*\
  !*** ./lib/utils/classNames.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   classNames: () => (/* binding */ classNames)
/* harmony export */ });
/*
    A utility for constructing a valid classnames string, you can either pass
    a string, or an object that maps a string to a boolean value, indicating if
    it should be included in the final object.

    For example:
        classNames('abc', '123') = 'abc 123'
        classNames('abc', {'123': true}) = 'abc 123'
        classNames('abc', {'123': false}) = 'abc'
*/
const classNames = (...args) => {
    let finalString = '';
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        // Skip undefined arguments
        if (arg === undefined) {
            continue;
        }
        if (typeof arg === 'string') {
            finalString += arg + ' ';
        }
        else {
            Object.entries(arg).map(([className, include]) => {
                if (include) {
                    finalString += className + ' ';
                }
            });
        }
    }
    return finalString;
};


/***/ }),

/***/ "./lib/utils/codeDiff.js":
/*!*******************************!*\
  !*** ./lib/utils/codeDiff.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createUnifiedDiff: () => (/* binding */ createUnifiedDiff),
/* harmony export */   getCodeDiffLineRanges: () => (/* binding */ getCodeDiffLineRanges),
/* harmony export */   getCodeDiffsAndUnifiedCodeString: () => (/* binding */ getCodeDiffsAndUnifiedCodeString)
/* harmony export */ });
/* harmony import */ var vscode_diff__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vscode-diff */ "webpack/sharing/consume/default/vscode-diff/vscode-diff");
/* harmony import */ var vscode_diff__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(vscode_diff__WEBPACK_IMPORTED_MODULE_0__);

const getCodeDiffLineRanges = (originalLines, modifiedLines) => {
    if (originalLines === undefined || originalLines === null) {
        originalLines = '';
    }
    if (modifiedLines === undefined || modifiedLines === null) {
        modifiedLines = '';
    }
    const originalLinesArray = originalLines.split('\n');
    const modifiedLinesArray = modifiedLines.split('\n');
    let options = {
        shouldPostProcessCharChanges: true,
        shouldIgnoreTrimWhitespace: true,
        shouldMakePrettyDiff: true,
        shouldComputeCharChanges: true,
        maxComputationTime: 0 // time in milliseconds, 0 => no computation limit.
    };
    let diffComputer = new vscode_diff__WEBPACK_IMPORTED_MODULE_0__.DiffComputer(originalLinesArray, modifiedLinesArray, options);
    let lineChanges = diffComputer.computeDiff().changes;
    return lineChanges || [];
};
const createUnifiedDiff = (originalCode, modifiedCode, lineChanges) => {
    if (originalCode === undefined || originalCode === null) {
        originalCode = '';
    }
    if (modifiedCode === undefined || modifiedCode === null) {
        modifiedCode = '';
    }
    const originalLines = originalCode.split('\n');
    const modifiedLines = modifiedCode.split('\n');
    /*
    Algorithm explanation:
    
    This function creates a unified diff by comparing the original and modified code.
    It iterates through both versions of the code simultaneously, creating a new representation
    of the code called result that is UnifiedDiffLine[]. Each time the algorithm sees a new line
    of code, it adds it to the result, marking it as unchanged, removed, or inserted.

    The algorithm works as follows:
    1. Process unchanged lines until a change is encountered.
    2. When a change is found, handle it based on its type:
        a. Modification: Mark original lines as removed, mark modified lines as inserted.
        b. Inserted: Add new lines from the modified code and mark as Inserted.
        c. Removed: Add removed lines from the original code to the result and mark as Removed.
    3. After processing all changes, handle any remaining lines.
    The result is a unified diff that shows all changes in context.
    */
    const result = [];
    let originalLineNum = 1;
    let modifiedLineNum = 1;
    let changeIndex = 0;
    while (originalLineNum <= originalLines.length ||
        modifiedLineNum <= modifiedLines.length) {
        if (changeIndex < lineChanges.length) {
            const change = lineChanges[changeIndex];
            // Process unchanged lines before the next change
            while ((originalLineNum < change.originalStartLineNumber ||
                modifiedLineNum < change.modifiedStartLineNumber) &&
                originalLineNum <= originalLines.length &&
                modifiedLineNum <= modifiedLines.length) {
                result.push({
                    content: originalLines[originalLineNum - 1],
                    type: 'unchanged',
                    originalLineNumber: originalLineNum,
                    modifiedLineNumber: modifiedLineNum,
                });
                originalLineNum++;
                modifiedLineNum++;
            }
            // Process the change
            if (change.originalEndLineNumber > 0 &&
                change.modifiedEndLineNumber > 0) {
                // Modification
                // First add removed lines
                for (; originalLineNum <= change.originalEndLineNumber; originalLineNum++) {
                    result.push({
                        content: originalLines[originalLineNum - 1],
                        type: 'removed',
                        originalLineNumber: originalLineNum,
                        modifiedLineNumber: null,
                    });
                }
                // Then add inserted lines
                for (; modifiedLineNum <= change.modifiedEndLineNumber; modifiedLineNum++) {
                    result.push({
                        content: modifiedLines[modifiedLineNum - 1],
                        type: 'inserted',
                        originalLineNumber: null,
                        modifiedLineNumber: modifiedLineNum,
                    });
                }
            }
            else if (change.originalEndLineNumber === 0) {
                // Inserted Lines
                for (; modifiedLineNum <= change.modifiedEndLineNumber; modifiedLineNum++) {
                    result.push({
                        content: modifiedLines[modifiedLineNum - 1],
                        type: 'inserted',
                        originalLineNumber: null,
                        modifiedLineNumber: modifiedLineNum,
                    });
                }
            }
            else if (change.modifiedEndLineNumber === 0) {
                // Removed lines
                for (; originalLineNum <= change.originalEndLineNumber; originalLineNum++) {
                    result.push({
                        content: originalLines[originalLineNum - 1],
                        type: 'removed',
                        originalLineNumber: originalLineNum,
                        modifiedLineNumber: null,
                    });
                }
            }
            changeIndex++;
        }
        else {
            // Process any remaining unchanged lines
            if (originalLineNum <= originalLines.length &&
                modifiedLineNum <= modifiedLines.length) {
                result.push({
                    content: originalLines[originalLineNum - 1],
                    type: 'unchanged',
                    originalLineNumber: originalLineNum,
                    modifiedLineNumber: modifiedLineNum,
                });
                originalLineNum++;
                modifiedLineNum++;
            }
            else if (originalLineNum <= originalLines.length) {
                // Remaining lines were removed
                result.push({
                    content: originalLines[originalLineNum - 1],
                    type: 'removed',
                    originalLineNumber: originalLineNum,
                    modifiedLineNumber: null,
                });
                originalLineNum++;
            }
            else if (modifiedLineNum <= modifiedLines.length) {
                // Remaining lines were added
                result.push({
                    content: modifiedLines[modifiedLineNum - 1],
                    type: 'inserted',
                    originalLineNumber: null,
                    modifiedLineNumber: modifiedLineNum,
                });
                modifiedLineNum++;
            }
            else {
                break;
            }
        }
    }
    return result;
};
const getCodeDiffsAndUnifiedCodeString = (originalCode, modifiedCode) => {
    const lineChanges = getCodeDiffLineRanges(originalCode, modifiedCode);
    const unifiedDiffs = createUnifiedDiff(originalCode, modifiedCode, lineChanges);
    const unifiedCodeString = (unifiedDiffs.map(line => {
        return line.content !== undefined ? line.content : '';
    }).join('\n'));
    return {
        unifiedCodeString,
        unifiedDiffs
    };
};


/***/ }),

/***/ "./lib/utils/handler.js":
/*!******************************!*\
  !*** ./lib/utils/handler.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Get the server settings
    const serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    // Construct the full URL
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(serverSettings.baseUrl, endPoint);
    // Add default headers
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    // Merge default headers with any provided headers
    init.headers = {
        ...defaultHeaders,
        ...init.headers,
    };
    // Make the request
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, serverSettings);
    }
    catch (error) {
        console.error('Error connecting to the mito_ai server:', error);
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    if (response.status === 401) {
        // This 401 error is set by the OpenAICompletionHandler class in the mito-ai python package.
        return {
            type: 'error',
            errorMessage: "You're missing the OPENAI_API_KEY environment variable. Run the following code in your terminal to set the environment variable and then relaunch the jupyter server ```python\nexport OPENAI_API_KEY=<your-api-key>\n```",
        };
    }
    if (response.status === 404) {
        // This 404 error is set by Jupyter when sending a request to the mito-ai endpoint that does not exist.
        return {
            type: 'error',
            errorMessage: "The Mito AI server is not enabled. You can enable it by running ```python\n!jupyter server extension enable mito-ai\n```",
        };
    }
    if (response.status === 500) {
        // This 500 error is set by the OpenAICompletionHandler class in the mito-ai python package. It is a 
        // generic error that is set when we haven't handled the error specifically.
        return {
            type: 'error',
            errorMessage: "There was an error communicating with OpenAI. This might be due to an incorrect API key, a temporary OpenAI outage, or a problem with your internet connection. Please try again.",
        };
    }
    // Handle the response
    let data = await response.text();
    try {
        data = JSON.parse(data);
        return {
            type: 'success',
            response: data
        };
    }
    catch (error) {
        console.error('Not a JSON response body.', response);
        return {
            type: 'error',
            errorMessage: "An error occurred while calling the Mito AI server",
        };
    }
}


/***/ }),

/***/ "./lib/utils/notebook.js":
/*!*******************************!*\
  !*** ./lib/utils/notebook.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getActiveCell: () => (/* binding */ getActiveCell),
/* harmony export */   getActiveCellCode: () => (/* binding */ getActiveCellCode),
/* harmony export */   getNotebookName: () => (/* binding */ getNotebookName),
/* harmony export */   writeCodeToActiveCell: () => (/* binding */ writeCodeToActiveCell)
/* harmony export */ });
/* harmony import */ var _strings__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./strings */ "./lib/utils/strings.js");

const getActiveCell = (notebookTracker) => {
    var _a;
    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
    const activeCell = notebook === null || notebook === void 0 ? void 0 : notebook.activeCell;
    return activeCell || undefined;
};
const getActiveCellCode = (notebookTracker) => {
    const activeCell = getActiveCell(notebookTracker);
    return activeCell === null || activeCell === void 0 ? void 0 : activeCell.model.sharedModel.source;
};
/*
    Writes code to the active cell in the notebook. If the code is undefined, it does nothing.
*/
const writeCodeToActiveCell = (notebookTracker, code, focus) => {
    if (code === undefined) {
        return;
    }
    const codeMirrorValidCode = (0,_strings__WEBPACK_IMPORTED_MODULE_0__.removeMarkdownCodeFormatting)(code);
    const activeCell = getActiveCell(notebookTracker);
    if (activeCell !== undefined) {
        activeCell.model.sharedModel.source = codeMirrorValidCode;
        if (focus) {
            activeCell.node.focus();
        }
    }
};
const getNotebookName = (notebookTracker) => {
    var _a;
    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
    return (notebook === null || notebook === void 0 ? void 0 : notebook.title.label) || 'Untitled';
};


/***/ }),

/***/ "./lib/utils/strings.js":
/*!******************************!*\
  !*** ./lib/utils/strings.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PYTHON_CODE_BLOCK_END_WITHOUT_NEW_LINE: () => (/* binding */ PYTHON_CODE_BLOCK_END_WITHOUT_NEW_LINE),
/* harmony export */   PYTHON_CODE_BLOCK_END_WITH_NEW_LINE: () => (/* binding */ PYTHON_CODE_BLOCK_END_WITH_NEW_LINE),
/* harmony export */   PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE: () => (/* binding */ PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE),
/* harmony export */   PYTHON_CODE_BLOCK_START_WITH_NEW_LINE: () => (/* binding */ PYTHON_CODE_BLOCK_START_WITH_NEW_LINE),
/* harmony export */   addMarkdownCodeFormatting: () => (/* binding */ addMarkdownCodeFormatting),
/* harmony export */   getCodeBlockFromMessage: () => (/* binding */ getCodeBlockFromMessage),
/* harmony export */   removeMarkdownCodeFormatting: () => (/* binding */ removeMarkdownCodeFormatting),
/* harmony export */   splitStringWithCodeBlocks: () => (/* binding */ splitStringWithCodeBlocks)
/* harmony export */ });
const PYTHON_CODE_BLOCK_START_WITH_NEW_LINE = '```python\n';
const PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE = '```python';
const PYTHON_CODE_BLOCK_END_WITH_NEW_LINE = '\n```';
const PYTHON_CODE_BLOCK_END_WITHOUT_NEW_LINE = '```';
/*
    Given a message from the OpenAI API, returns the content as a string.
    If the content is not a string, returns undefined.
*/
const getContentStringFromMessage = (message) => {
    // TODO: We can't assume this is a string. We need to handle the other
    // return options
    if (message.role === 'user' || message.role === 'assistant') {
        return message.content;
    }
    return undefined;
};
/*
    Given a string like "Hello ```python print('Hello, world!')```",
    returns ["Hello", "```python print('Hello, world!')```"]

    This is useful for taking an AI generated message and displaying the code in
    code blocks and the rest of the message in plain text.
*/
const splitStringWithCodeBlocks = (message) => {
    const messageContent = getContentStringFromMessage(message);
    if (!messageContent) {
        return [];
    }
    const parts = messageContent.split(/(```[\s\S]*?```)/);
    // Remove empty strings caused by consecutive delimiters, if any
    return parts.filter(part => part.trim() !== "");
};
/*
    Given a string like "Hello ```python print('Hello, world!')```",
    returns "```python print('Hello, world!')```"
*/
const getCodeBlockFromMessage = (message) => {
    const parts = splitStringWithCodeBlocks(message);
    return parts.find(part => part.startsWith('```'));
};
/*
    To display code in markdown, we need to take input values like this:

    ```python x + 1```

    And turn them into this:

    ```python
    x + 1
    ```

    Sometimes, we also want to trim the code to remove any leading or trailing whitespace. For example,
    when we're displaying the code in the chat history this is useful. Othertimes we don't want to trim.
    For example, when we're displaying the code in the active cell, we want to keep the users's whitespace.
    This is important for showing diffs. If the code cell contains no code, the first line will be marked as
    removed in the code diff. To ensure the diff lines up with the code, we need to leave this whitespace line.
*/
const addMarkdownCodeFormatting = (code, trim) => {
    let codeWithoutBackticks = code;
    // If the code already has the code formatting backticks, remove them 
    // so we can add them back in the correct format
    if (code.split(PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE).length > 1) {
        codeWithoutBackticks = code.split(PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE)[1].split(PYTHON_CODE_BLOCK_END_WITHOUT_NEW_LINE)[0];
    }
    else {
        codeWithoutBackticks = code;
    }
    if (trim) {
        codeWithoutBackticks = codeWithoutBackticks.trim();
    }
    // Note: We add a space after the code because for some unknown reason, the markdown 
    // renderer is cutting off the last character in the code block.
    return `${PYTHON_CODE_BLOCK_START_WITH_NEW_LINE}${codeWithoutBackticks} ${PYTHON_CODE_BLOCK_END_WITH_NEW_LINE}`;
};
/*
    To write code in a Jupyter Code Cell, we need to take inputs like this:

    ```python
    x + 1
    ```

    And turn them into this:

    x + 1

    Jupyter does not need the backticks.
*/
const removeMarkdownCodeFormatting = (code) => {
    if (code.split(PYTHON_CODE_BLOCK_START_WITHOUT_NEW_LINE).length > 1) {
        return code.split(PYTHON_CODE_BLOCK_START_WITH_NEW_LINE)[1].split(PYTHON_CODE_BLOCK_END_WITH_NEW_LINE)[0];
    }
    return code;
};


/***/ }),

/***/ "./lib/utils/user.js":
/*!***************************!*\
  !*** ./lib/utils/user.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getOperatingSystem: () => (/* binding */ getOperatingSystem)
/* harmony export */ });
const getOperatingSystem = () => {
    if (navigator.userAgent.includes('Macintosh')) {
        return 'mac';
    }
    else {
        return 'windows';
    }
};


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/ChatTaskpane.css":
/*!**********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/ChatTaskpane.css ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.chat-taskpane {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: var(--chat-background-color) !important;
    --jp-sidebar-min-width: 350px;
    width: 100%;
    box-sizing: border-box;
    overflow-y: scroll;

    /* 
        Don't set padding on top from the taskpane so we can instead
        set the padding on the chat-taskpane-header instead to make 
        sure the sticky header covers all of the content behind it. 
    */
    padding-top: 0px; 
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 10px;
}

.chat-taskpane-header {
    display: flex;
    flex-direction: row;
    justify-content: end;
    align-items: center;
    padding-top: 10px;
    padding-bottom: 5px;
    position: sticky; /* Make the header sticky */
    top: 0; /* Stick to the top of the container */
    background-color: var(--chat-background-color); /* Ensure background color covers content behind */
    z-index: 1; /* Ensure it stays above other content */
}

.chat-taskpane-header-title {
    font-size: 14px;
    font-weight: bold;
    margin: 0;
}

.message {
    height: min-content;
    margin-bottom: 10px;
    box-sizing: border-box;
    padding: 10px;
    width: 100%;
    font-size: 14px;
}

.message-user {
    background-color: var(--chat-user-message-background-color); 
    color: var(--chat-user-message-font-color);
    border-radius: 5px;
}

.message-assistant {
    color: var(--chat-assistant-message-font-color);
}

.chat-input {
    outline: none;
    border: none;
    resize: none;
    width: 100%;
    padding: 10px;
    overflow-y: hidden;
    box-sizing: border-box;

    /* 
        The height of the chat input is set in the ChatTaskpane.tsx file. 
        See the adjustHeight function for more detail.
    */
    flex-shrink: 0 !important; 
}

.chat-loading-message {
    margin-top: 20px;
    margin-bottom: 20px;
}

.message-text {
    align-items: center;
}
`, "",{"version":3,"sources":["webpack://./style/ChatTaskpane.css"],"names":[],"mappings":"AAAA;IACI,aAAa;IACb,sBAAsB;IACtB,YAAY;IACZ,yDAAyD;IACzD,6BAA6B;IAC7B,WAAW;IACX,sBAAsB;IACtB,kBAAkB;;IAElB;;;;KAIC;IACD,gBAAgB;IAChB,kBAAkB;IAClB,mBAAmB;IACnB,oBAAoB;AACxB;;AAEA;IACI,aAAa;IACb,mBAAmB;IACnB,oBAAoB;IACpB,mBAAmB;IACnB,iBAAiB;IACjB,mBAAmB;IACnB,gBAAgB,EAAE,2BAA2B;IAC7C,MAAM,EAAE,sCAAsC;IAC9C,8CAA8C,EAAE,kDAAkD;IAClG,UAAU,EAAE,wCAAwC;AACxD;;AAEA;IACI,eAAe;IACf,iBAAiB;IACjB,SAAS;AACb;;AAEA;IACI,mBAAmB;IACnB,mBAAmB;IACnB,sBAAsB;IACtB,aAAa;IACb,WAAW;IACX,eAAe;AACnB;;AAEA;IACI,2DAA2D;IAC3D,0CAA0C;IAC1C,kBAAkB;AACtB;;AAEA;IACI,+CAA+C;AACnD;;AAEA;IACI,aAAa;IACb,YAAY;IACZ,YAAY;IACZ,WAAW;IACX,aAAa;IACb,kBAAkB;IAClB,sBAAsB;;IAEtB;;;KAGC;IACD,yBAAyB;AAC7B;;AAEA;IACI,gBAAgB;IAChB,mBAAmB;AACvB;;AAEA;IACI,mBAAmB;AACvB","sourcesContent":[".chat-taskpane {\n    display: flex;\n    flex-direction: column;\n    height: 100%;\n    background-color: var(--chat-background-color) !important;\n    --jp-sidebar-min-width: 350px;\n    width: 100%;\n    box-sizing: border-box;\n    overflow-y: scroll;\n\n    /* \n        Don't set padding on top from the taskpane so we can instead\n        set the padding on the chat-taskpane-header instead to make \n        sure the sticky header covers all of the content behind it. \n    */\n    padding-top: 0px; \n    padding-left: 10px;\n    padding-right: 10px;\n    padding-bottom: 10px;\n}\n\n.chat-taskpane-header {\n    display: flex;\n    flex-direction: row;\n    justify-content: end;\n    align-items: center;\n    padding-top: 10px;\n    padding-bottom: 5px;\n    position: sticky; /* Make the header sticky */\n    top: 0; /* Stick to the top of the container */\n    background-color: var(--chat-background-color); /* Ensure background color covers content behind */\n    z-index: 1; /* Ensure it stays above other content */\n}\n\n.chat-taskpane-header-title {\n    font-size: 14px;\n    font-weight: bold;\n    margin: 0;\n}\n\n.message {\n    height: min-content;\n    margin-bottom: 10px;\n    box-sizing: border-box;\n    padding: 10px;\n    width: 100%;\n    font-size: 14px;\n}\n\n.message-user {\n    background-color: var(--chat-user-message-background-color); \n    color: var(--chat-user-message-font-color);\n    border-radius: 5px;\n}\n\n.message-assistant {\n    color: var(--chat-assistant-message-font-color);\n}\n\n.chat-input {\n    outline: none;\n    border: none;\n    resize: none;\n    width: 100%;\n    padding: 10px;\n    overflow-y: hidden;\n    box-sizing: border-box;\n\n    /* \n        The height of the chat input is set in the ChatTaskpane.tsx file. \n        See the adjustHeight function for more detail.\n    */\n    flex-shrink: 0 !important; \n}\n\n.chat-loading-message {\n    margin-top: 20px;\n    margin-bottom: 20px;\n}\n\n.message-text {\n    align-items: center;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/CodeMessagePart.css":
/*!*************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/CodeMessagePart.css ***!
  \*************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.code-message-part-container {
    display: flex;
    flex-direction: column;

    background-color: var(--chat-background-color);
    border-radius: 3px;
    border: 1px solid var(--chat-user-message-font-color);
    overflow: hidden;
}

.code-message-part-toolbar {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    width: 100%;
    background-color: var(--chat-user-message-background-color);
    border-bottom: 1px solid var(--chat-user-message-font-color);
    font-size: 0.8em;
}

.code-location {
    flex-grow: 1;
    margin-left: 5px;
    color: var(--chat-user-message-font-color);
}

.code-message-part-toolbar button {
    background-color: var(--chat-user-message-background-color);
    border: none;
    border-left: 1px solid var(--chat-user-message-font-color);
    border-radius: 0px;

    font-size: 0.8em;
    color: var(--chat-user-message-font-color);
}

.code-message-part-toolbar button:hover {
    background-color: var(--chat-background-color);
    color: var(--chat-assistant-message-font-color);
}`, "",{"version":3,"sources":["webpack://./style/CodeMessagePart.css"],"names":[],"mappings":"AAAA;IACI,aAAa;IACb,sBAAsB;;IAEtB,8CAA8C;IAC9C,kBAAkB;IAClB,qDAAqD;IACrD,gBAAgB;AACpB;;AAEA;IACI,aAAa;IACb,mBAAmB;IACnB,mBAAmB;IACnB,uBAAuB;;IAEvB,WAAW;IACX,2DAA2D;IAC3D,4DAA4D;IAC5D,gBAAgB;AACpB;;AAEA;IACI,YAAY;IACZ,gBAAgB;IAChB,0CAA0C;AAC9C;;AAEA;IACI,2DAA2D;IAC3D,YAAY;IACZ,0DAA0D;IAC1D,kBAAkB;;IAElB,gBAAgB;IAChB,0CAA0C;AAC9C;;AAEA;IACI,8CAA8C;IAC9C,+CAA+C;AACnD","sourcesContent":[".code-message-part-container {\n    display: flex;\n    flex-direction: column;\n\n    background-color: var(--chat-background-color);\n    border-radius: 3px;\n    border: 1px solid var(--chat-user-message-font-color);\n    overflow: hidden;\n}\n\n.code-message-part-toolbar {\n    display: flex;\n    flex-direction: row;\n    align-items: center;\n    justify-content: center;\n\n    width: 100%;\n    background-color: var(--chat-user-message-background-color);\n    border-bottom: 1px solid var(--chat-user-message-font-color);\n    font-size: 0.8em;\n}\n\n.code-location {\n    flex-grow: 1;\n    margin-left: 5px;\n    color: var(--chat-user-message-font-color);\n}\n\n.code-message-part-toolbar button {\n    background-color: var(--chat-user-message-background-color);\n    border: none;\n    border-left: 1px solid var(--chat-user-message-font-color);\n    border-radius: 0px;\n\n    font-size: 0.8em;\n    color: var(--chat-user-message-font-color);\n}\n\n.code-message-part-toolbar button:hover {\n    background-color: var(--chat-background-color);\n    color: var(--chat-assistant-message-font-color);\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/ErrorMimeRendererPlugin.css":
/*!*********************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/ErrorMimeRendererPlugin.css ***!
  \*********************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.error-mime-renderer-container {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: start;
    background-color: var(--jp-rendermime-error-background);
    width: 100%;
}

.error-mime-renderer-button {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;

    background-color: var(--jp-error-color3);
    border: var(--jp-error-color0) 1px solid;
    color: var(--jp-error-color0);

    margin: 10px;
    box-sizing: border-box;

    border-radius: 3px;
    font-size: 14px;
}

.error-mime-renderer-button svg {
    margin-right: 5px;
}

.error-mime-renderer-button p {
    margin: 0;
}

`, "",{"version":3,"sources":["webpack://./style/ErrorMimeRendererPlugin.css"],"names":[],"mappings":"AAAA;IACI,aAAa;IACb,mBAAmB;IACnB,sBAAsB;IACtB,kBAAkB;IAClB,uDAAuD;IACvD,WAAW;AACf;;AAEA;IACI,aAAa;IACb,mBAAmB;IACnB,sBAAsB;IACtB,mBAAmB;;IAEnB,wCAAwC;IACxC,wCAAwC;IACxC,6BAA6B;;IAE7B,YAAY;IACZ,sBAAsB;;IAEtB,kBAAkB;IAClB,eAAe;AACnB;;AAEA;IACI,iBAAiB;AACrB;;AAEA;IACI,SAAS;AACb","sourcesContent":[".error-mime-renderer-container {\n    display: flex;\n    flex-direction: row;\n    justify-content: start;\n    align-items: start;\n    background-color: var(--jp-rendermime-error-background);\n    width: 100%;\n}\n\n.error-mime-renderer-button {\n    display: flex;\n    flex-direction: row;\n    justify-content: start;\n    align-items: center;\n\n    background-color: var(--jp-error-color3);\n    border: var(--jp-error-color0) 1px solid;\n    color: var(--jp-error-color0);\n\n    margin: 10px;\n    box-sizing: border-box;\n\n    border-radius: 3px;\n    font-size: 14px;\n}\n\n.error-mime-renderer-button svg {\n    margin-right: 5px;\n}\n\n.error-mime-renderer-button p {\n    margin: 0;\n}\n\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/IconButton.css":
/*!********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/IconButton.css ***!
  \********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.icon-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
}`, "",{"version":3,"sources":["webpack://./style/IconButton.css"],"names":[],"mappings":"AAAA;IACI,6BAA6B;IAC7B,YAAY;IACZ,eAAe;AACnB","sourcesContent":[".icon-button {\n    background-color: transparent;\n    border: none;\n    cursor: pointer;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/PythonCode.css":
/*!********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/PythonCode.css ***!
  \********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.code-message-part-python-code pre {
    flex-grow: 1;
    height: 100%;
    width: 100%;
    margin: 0 !important;
    padding: 10px !important;
    font-size: 12px !important;
    overflow-x: auto;
}

.code-message-part-python-code code {
    white-space: pre !important;
}

.code-message-part-python-code .jp-RenderedHTMLCommon > *:last-child {
    /* 
        Remove the default Jupyter ending margin 
        so that the rendered code is flush with the bottom
        of the CodeMessagePart
    */
    margin-bottom: 0px;
}`, "",{"version":3,"sources":["webpack://./style/PythonCode.css"],"names":[],"mappings":"AAAA;IACI,YAAY;IACZ,YAAY;IACZ,WAAW;IACX,oBAAoB;IACpB,wBAAwB;IACxB,0BAA0B;IAC1B,gBAAgB;AACpB;;AAEA;IACI,2BAA2B;AAC/B;;AAEA;IACI;;;;KAIC;IACD,kBAAkB;AACtB","sourcesContent":[".code-message-part-python-code pre {\n    flex-grow: 1;\n    height: 100%;\n    width: 100%;\n    margin: 0 !important;\n    padding: 10px !important;\n    font-size: 12px !important;\n    overflow-x: auto;\n}\n\n.code-message-part-python-code code {\n    white-space: pre !important;\n}\n\n.code-message-part-python-code .jp-RenderedHTMLCommon > *:last-child {\n    /* \n        Remove the default Jupyter ending margin \n        so that the rendered code is flush with the bottom\n        of the CodeMessagePart\n    */\n    margin-bottom: 0px;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/ChatTaskpane.css":
/*!********************************!*\
  !*** ./style/ChatTaskpane.css ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./ChatTaskpane.css */ "./node_modules/css-loader/dist/cjs.js!./style/ChatTaskpane.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/CodeMessagePart.css":
/*!***********************************!*\
  !*** ./style/CodeMessagePart.css ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./CodeMessagePart.css */ "./node_modules/css-loader/dist/cjs.js!./style/CodeMessagePart.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/ErrorMimeRendererPlugin.css":
/*!*******************************************!*\
  !*** ./style/ErrorMimeRendererPlugin.css ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./ErrorMimeRendererPlugin.css */ "./node_modules/css-loader/dist/cjs.js!./style/ErrorMimeRendererPlugin.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/IconButton.css":
/*!******************************!*\
  !*** ./style/IconButton.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./IconButton.css */ "./node_modules/css-loader/dist/cjs.js!./style/IconButton.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/PythonCode.css":
/*!******************************!*\
  !*** ./style/PythonCode.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./PythonCode.css */ "./node_modules/css-loader/dist/cjs.js!./style/PythonCode.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./src/icons/ChatIcon.svg":
/*!********************************!*\
  !*** ./src/icons/ChatIcon.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg width=\"19\" height=\"20\" viewBox=\"0 0 19 20\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n    <path d=\"M15.0626 4.8125C15.5466 4.8125 15.9376 5.20352 15.9376 5.6875C15.9376 6.17148 15.5466 6.5625 15.0626 6.5625C14.5787 6.5625 14.1876 6.17148 14.1876 5.6875C14.1876 5.20352 14.5787 4.8125 15.0626 4.8125ZM12.0001 4.8125C12.4841 4.8125 12.8751 5.20352 12.8751 5.6875C12.8751 6.17148 12.4841 6.5625 12.0001 6.5625C11.5162 6.5625 11.1251 6.17148 11.1251 5.6875C11.1251 5.20352 11.5162 4.8125 12.0001 4.8125ZM8.93764 4.8125C9.42162 4.8125 9.81264 5.20352 9.81264 5.6875C9.81264 6.17148 9.42162 6.5625 8.93764 6.5625C8.45365 6.5625 8.06264 6.17148 8.06264 5.6875C8.06264 5.20352 8.45365 4.8125 8.93764 4.8125ZM12.0001 0C15.8665 0 19.0001 2.5457 19.0001 5.6875C19.0001 6.98906 18.456 8.18125 17.5537 9.14102C17.9611 10.2184 18.8087 11.1316 18.8224 11.1426C19.0029 11.334 19.0521 11.6129 18.9482 11.8535C18.8443 12.0941 18.6064 12.25 18.3439 12.25C16.6622 12.25 15.3361 11.5473 14.5404 10.984C13.7501 11.2328 12.897 11.375 12.0001 11.375C8.13373 11.375 5.00014 8.8293 5.00014 5.6875C5.00014 2.5457 8.13373 0 12.0001 0ZM12.0001 10.0625C12.7302 10.0625 13.4521 9.95039 14.1439 9.73164L14.7646 9.53477L15.2978 9.91211C15.6888 10.1883 16.2247 10.4973 16.8701 10.7051C16.6705 10.3742 16.4763 10.0023 16.3259 9.60586L16.0361 8.8375L16.5994 8.24141C17.0943 7.71367 17.6876 6.84141 17.6876 5.6875C17.6876 3.27578 15.1365 1.3125 12.0001 1.3125C8.86381 1.3125 6.31264 3.27578 6.31264 5.6875C6.31264 8.09922 8.86381 10.0625 12.0001 10.0625Z\" fill=\"black\"/>\n    <path d=\"M7 7C3.13359 7 0 9.5457 0 12.6875C0 14.0437 0.585156 15.2852 1.55859 16.2613C1.2168 17.6395 0.0738281 18.8672 0.0601563 18.8809C0 18.9438 -0.0164062 19.0367 0.0191406 19.1188C0.0546875 19.2008 0.13125 19.25 0.21875 19.25C2.03164 19.25 3.39063 18.3805 4.06328 17.8445C4.95742 18.1809 5.95 18.375 7 18.375C10.8664 18.375 14 15.8293 14 12.6875C14 9.5457 10.8664 7 7 7ZM3.5 13.5625C3.01602 13.5625 2.625 13.1715 2.625 12.6875C2.625 12.2035 3.01602 11.8125 3.5 11.8125C3.98398 11.8125 4.375 12.2035 4.375 12.6875C4.375 13.1715 3.98398 13.5625 3.5 13.5625ZM7 13.5625C6.51602 13.5625 6.125 13.1715 6.125 12.6875C6.125 12.2035 6.51602 11.8125 7 11.8125C7.48398 11.8125 7.875 12.2035 7.875 12.6875C7.875 13.1715 7.48398 13.5625 7 13.5625ZM10.5 13.5625C10.016 13.5625 9.625 13.1715 9.625 12.6875C9.625 12.2035 10.016 11.8125 10.5 11.8125C10.984 11.8125 11.375 12.2035 11.375 12.6875C11.375 13.1715 10.984 13.5625 10.5 13.5625Z\" fill=\"black\"/>\n</svg>\n";

/***/ }),

/***/ "./src/icons/LightbulbIcon.svg":
/*!*************************************!*\
  !*** ./src/icons/LightbulbIcon.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg width=\"1200pt\" height=\"1200pt\" version=\"1.1\" viewBox=\"0 0 1200 1200\" xmlns=\"http://www.w3.org/2000/svg\">\n <path d=\"m735.61 979.22h-271.22c-19.781 0-33.844 14.391-33.844 34.688s14.156 34.688 33.844 34.688h271.22c19.781 0 33.844-14.391 33.844-34.688s-14.156-34.688-33.844-34.688z\" fill=\"#9c6bff\"/>\n <path d=\"m735.61 891.84h-271.22c-19.781 0-33.844 13.922-33.844 33.375 0 16.688 14.156 33.375 33.844 33.375h271.22c19.781 0 33.844-16.688 33.844-33.375 0-19.453-14.156-33.375-33.844-33.375z\" fill=\"#9c6bff\"/>\n <path d=\"m701.86 1070.6h-203.86c-5.625 0-8.5312 2.8594-2.8594 8.625l51 51.938c5.625 2.8594 14.156 8.625 19.781 8.625h67.922c5.625 0 14.156-5.7656 19.781-8.625l51-51.938c5.625-5.7656 2.8594-8.625-2.8594-8.625z\" fill=\"#9c6bff\"/>\n <path d=\"m600 60c-187.78 0-341.53 153.84-341.53 341.76 0 74.062 22.781 145.22 62.625 199.31 48.375 79.781 108.14 162.37 108.14 250.69v5.625c0 5.625 5.625 11.391 11.391 11.391h318.71c5.625 0 11.391-5.625 11.391-11.391v-5.625c0-91.078 65.391-176.53 113.86-256.31 36.938-54.141 56.859-122.53 56.859-193.69 0-187.92-153.71-341.76-341.53-341.76zm-23.531 138.14c-98.391 0-178.45 80.062-178.45 178.45 0 10.453-8.5312 18.938-18.938 18.938-10.453 0-18.938-8.5312-18.938-18.938 0-119.3 97.078-216.37 216.37-216.37 10.453 0 18.938 8.5312 18.938 18.938 0 10.453-8.5312 18.938-18.938 18.938z\" fill=\"#9c6bff\"/>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.d58115937b8dbc9496c3.js.map