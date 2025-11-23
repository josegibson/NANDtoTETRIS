import React from 'react';
import './Layout.css';

interface LayoutProps {
    children: React.ReactNode;
    onCompile: () => void;
    isCompiling: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, onCompile, isCompiling }) => {
    return (
        <div className="layout">
            <header className="header">
                <div className="logo">Jack Visualizer</div>
                <div className="controls">
                    <input type="text" defaultValue="MyPongGame" className="project-name" />
                    <button className="compile-btn" onClick={onCompile} disabled={isCompiling}>
                        {isCompiling ? 'Compiling...' : '▶ Compile Project'}
                    </button>
                </div>
            </header>
            <main className="main-content">
                {children}
            </main>
            <footer className="footer">
                <div className="status">Ready</div>
            </footer>
        </div>
    );
};
