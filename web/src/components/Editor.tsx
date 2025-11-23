import React, { useEffect } from 'react';
import Editor, { useMonaco } from '@monaco-editor/react';
import './Editor.css';

interface CodeEditorProps {
    fileName: string;
    code: string;
    onChange: (value: string | undefined) => void;
    readOnly?: boolean;
    language?: string;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({
    fileName,
    code,
    onChange,
    readOnly = false,
    language = 'jack',
}) => {
    const monaco = useMonaco();

    useEffect(() => {
        if (monaco) {
            // Register Jack language
            if (!monaco.languages.getLanguages().some((l) => l.id === 'jack')) {
                monaco.languages.register({ id: 'jack' });
                monaco.languages.setMonarchTokensProvider('jack', {
                    keywords: [
                        'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
                        'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
                        'let', 'do', 'if', 'else', 'while', 'return'
                    ],
                    tokenizer: {
                        root: [
                            [/[a-zA-Z_]\w*/, {
                                cases: {
                                    '@keywords': 'keyword',
                                    '@default': 'identifier'
                                }
                            }],
                            [/\d+/, 'number'],
                            [/"[^"]*"/, 'string'],
                            [/\/\/.*/, 'comment'],
                            [/\/\*[\s\S]*?\*\//, 'comment'],
                            [/[{}()\[\]]/, 'delimiter'],
                            [/[=;.,+\-*/&|~<>]/, 'delimiter'],
                        ],
                    },
                });
            }

            // Register VM language
            if (!monaco.languages.getLanguages().some((l) => l.id === 'vm')) {
                monaco.languages.register({ id: 'vm' });
                monaco.languages.setMonarchTokensProvider('vm', {
                    keywords: [
                        'push', 'pop', 'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not',
                        'label', 'goto', 'if-goto', 'function', 'call', 'return',
                        'local', 'argument', 'this', 'that', 'constant', 'static', 'pointer', 'temp'
                    ],
                    tokenizer: {
                        root: [
                            [/[a-zA-Z_][\w\.]*/, {
                                cases: {
                                    '@keywords': 'keyword',
                                    '@default': 'identifier'
                                }
                            }],
                            [/\d+/, 'number'],
                            [/\/\/.*/, 'comment'],
                        ],
                    },
                });
            }
        }
    }, [monaco]);

    return (
        <div className="editor-container">
            <div className="editor-header">
                <span>{fileName}</span>
                {readOnly && <span className="readonly-badge">READ ONLY</span>}
            </div>
            <Editor
                height="100%"
                language={language}
                theme="vs-dark"
                value={code}
                onChange={onChange}
                options={{
                    readOnly,
                    minimap: { enabled: false },
                    fontSize: 14,
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                }}
            />
        </div>
    );
};
