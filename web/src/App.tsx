import { useState } from 'react';
import { Layout } from './components/Layout';
import { SplitPane } from './components/SplitPane';
import { FileExplorer, FileItem } from './components/FileExplorer';
import { CodeEditor } from './components/Editor';
import { OutputTabs, CompilationResult, OutputTab } from './components/OutputTabs';
import './App.css';

const DEFAULT_FILES: FileItem[] = [
    {
        name: 'Main.jack',
        content: `class Main {
    function void main() {
        var int i, sum;
        let i = 0;
        let sum = 0;
        
        while (i < 10) {
            let sum = sum + i;
            let i = i + 1;
        }
        
        do Output.printString("Sum is: ");
        do Output.printInt(sum);
        do Output.println();
        return;
    }
}`
    }
];

function App() {
    const [files, setFiles] = useState<FileItem[]>(DEFAULT_FILES);
    const [activeFileName, setActiveFileName] = useState<string>('Main.jack');
    const [compilationResult, setCompilationResult] = useState<CompilationResult | null>(null);
    const [isCompiling, setIsCompiling] = useState(false);
    const [activeTab, setActiveTab] = useState<OutputTab>('vm');

    const activeFile = files.find(f => f.name === activeFileName);

    const handleFileSelect = (fileName: string) => {
        setActiveFileName(fileName);
    };

    const handleFileAdd = () => {
        const newName = prompt('Enter file name (e.g. Square.jack):');
        if (newName && !files.some(f => f.name === newName)) {
            setFiles([...files, { name: newName, content: '' }]);
            setActiveFileName(newName);
        }
    };

    const handleFileDelete = (fileName: string) => {
        if (confirm(`Are you sure you want to delete ${fileName}?`)) {
            const newFiles = files.filter(f => f.name !== fileName);
            setFiles(newFiles);
            if (activeFileName === fileName && newFiles.length > 0) {
                setActiveFileName(newFiles[0].name);
            }
        }
    };

    const handleCodeChange = (value: string | undefined) => {
        if (value === undefined) return;
        setFiles(files.map(f =>
            f.name === activeFileName ? { ...f, content: value } : f
        ));
    };

    const handleCompile = async () => {
        setIsCompiling(true);
        setCompilationResult(null);

        try {
            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
            const response = await fetch(`${apiUrl}/compile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ files }),
            });

            const data = await response.json();

            if (response.ok) {
                setCompilationResult({
                    vm: data.vm,
                    asm: data.asm,
                    hack: data.hack,
                });
                setActiveTab('vm');
            } else {
                setCompilationResult({
                    vm: [],
                    asm: '',
                    hack: '',
                    error: data.error || 'Unknown compilation error',
                });
            }
        } catch (error) {
            setCompilationResult({
                vm: [],
                asm: '',
                hack: '',
                error: `Network Error: ${error instanceof Error ? error.message : String(error)}. Is the backend server running?`,
            });
        } finally {
            setIsCompiling(false);
        }
    };



    return (
        <Layout onCompile={handleCompile} isCompiling={isCompiling}>
            <SplitPane
                left={
                    <div style={{ display: 'flex', height: '100%' }}>
                        <div style={{ width: '200px', flexShrink: 0 }}>
                            <FileExplorer
                                files={files}
                                activeFile={activeFileName}
                                onFileSelect={handleFileSelect}
                                onFileAdd={handleFileAdd}
                                onFileDelete={handleFileDelete}
                            />
                        </div>
                        <div style={{ flex: 1 }}>
                            {activeFile ? (
                                <CodeEditor
                                    fileName={activeFile.name}
                                    code={activeFile.content}
                                    onChange={handleCodeChange}
                                />
                            ) : (
                                <div className="no-file-selected">Select a file to edit</div>
                            )}
                        </div>
                    </div>
                }
                right={
                    <OutputTabs
                        result={compilationResult}
                        activeTab={activeTab}
                        onTabChange={setActiveTab}
                    />
                }
            />
        </Layout>
    );
}

export default App;
