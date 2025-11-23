import React from 'react';
import './FileExplorer.css';

export interface FileItem {
    name: string;
    content: string;
}

interface FileExplorerProps {
    files: FileItem[];
    activeFile: string | null;
    onFileSelect: (fileName: string) => void;
    onFileAdd: () => void;
    onFileDelete: (fileName: string) => void;
}

export const FileExplorer: React.FC<FileExplorerProps> = ({
    files,
    activeFile,
    onFileSelect,
    onFileAdd,
    onFileDelete,
}) => {
    return (
        <div className="file-explorer">
            <div className="explorer-header">
                <span>FILES</span>
                <button className="add-file-btn" onClick={onFileAdd} title="Add New File">
                    +
                </button>
            </div>
            <ul className="file-list">
                {files.map((file) => (
                    <li
                        key={file.name}
                        className={`file-item ${activeFile === file.name ? 'active' : ''}`}
                        onClick={() => onFileSelect(file.name)}
                    >
                        <span className="file-icon">J</span>
                        <span className="file-name">{file.name}</span>
                        {file.name !== 'Main.jack' && (
                            <button
                                className="delete-file-btn"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onFileDelete(file.name);
                                }}
                                title="Delete File"
                            >
                                ×
                            </button>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};
