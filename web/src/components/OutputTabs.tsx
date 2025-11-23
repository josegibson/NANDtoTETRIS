import React, { useState } from 'react';
import { CodeEditor } from './Editor';
import { VMEmulator } from './VMEmulator';
import { VerticalSplitPane } from './VerticalSplitPane';
import './OutputTabs.css';

export interface CompilationResult {
    vm: { name: string; content: string }[];
    asm: string;
    hack: string;
    error?: string;
}

export type OutputTab = 'vm' | 'asm' | 'hack';

interface OutputTabsProps {
    result: CompilationResult | null;
    activeTab: OutputTab;
    onTabChange: (tab: OutputTab) => void;
}

export const OutputTabs: React.FC<OutputTabsProps> = ({ result, activeTab, onTabChange }) => {
    const [activeVmFile, setActiveVmFile] = useState<string>('');

    // Update active VM file when result changes
    React.useEffect(() => {
        if (result?.vm && result.vm.length > 0) {
            setActiveVmFile(result.vm[0].name);
        }
    }, [result]);

    if (!result) {
        return (
            <div className="output-placeholder">
                <div className="placeholder-content">
                    <h3>Ready to Compile</h3>
                    <p>Click the "Compile Project" button to generate VM, Assembly, and Hack code.</p>
                </div>
            </div>
        );
    }

    if (result.error) {
        return (
            <div className="output-error">
                <h3>Compilation Failed</h3>
                <pre>{result.error}</pre>
            </div>
        );
    }

    const renderCodeContent = () => {
        switch (activeTab) {
            case 'vm':
                const vmFile = result.vm.find(f => f.name === activeVmFile);
                return (
                    <div className="tab-content">
                        {result.vm.length > 1 && (
                            <div className="sub-nav">
                                <select
                                    value={activeVmFile}
                                    onChange={(e) => setActiveVmFile(e.target.value)}
                                    className="vm-selector"
                                >
                                    {result.vm.map(f => (
                                        <option key={f.name} value={f.name}>{f.name}</option>
                                    ))}
                                </select>
                            </div>
                        )}
                        <div className="code-view">
                            <CodeEditor
                                fileName={activeVmFile || 'Output.vm'}
                                code={vmFile?.content || ''}
                                onChange={() => { }}
                                readOnly={true}
                                language="vm"
                            />
                        </div>
                    </div>
                );
            case 'asm':
                return (
                    <div className="tab-content">
                        <CodeEditor
                            fileName="Project.asm"
                            code={result.asm}
                            onChange={() => { }}
                            readOnly={true}
                            language="text" // No ASM syntax highlighting yet
                        />
                    </div>
                );
            case 'hack':
                return (
                    <div className="tab-content hack-view">
                        <div className="hack-grid-header">
                            <span className="col-addr">Addr</span>
                            <span className="col-instr">Instruction</span>
                        </div>
                        <div className="hack-grid">
                            {result.hack.split('\n').map((line, idx) => {
                                if (!line.trim()) return null;
                                const isCInstruction = line.trim().startsWith('1');
                                return (
                                    <div key={idx} className="hack-row">
                                        <span className="col-addr">{idx}</span>
                                        <span className={`col-instr ${isCInstruction ? 'c-instr' : 'a-instr'}`}>
                                            {line.trim()}
                                        </span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                );
        }
    };

    const topSection = (
        <div className="output-tabs">
            <div className="tabs-header">
                <button
                    className={`tab-btn ${activeTab === 'vm' ? 'active' : ''}`}
                    onClick={() => onTabChange('vm')}
                >
                    VM Code
                </button>

                <button
                    className={`tab-btn ${activeTab === 'asm' ? 'active' : ''}`}
                    onClick={() => onTabChange('asm')}
                >
                    Assembly
                </button>
                <button
                    className={`tab-btn ${activeTab === 'hack' ? 'active' : ''}`}
                    onClick={() => onTabChange('hack')}
                >
                    Binary
                </button>
            </div>
            <div className="tabs-body">
                {renderCodeContent()}
            </div>
        </div>
    );

    const bottomSection = (
        <div style={{ height: '100%', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
            <VMEmulator vmFiles={result.vm} />
        </div>
    );

    return (
        <VerticalSplitPane
            top={topSection}
            bottom={bottomSection}
            initialSplit={50}
        />
    );
};
