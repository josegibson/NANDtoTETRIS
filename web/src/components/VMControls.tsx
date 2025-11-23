import React from 'react';

interface VMControlsProps {
    isRunning: boolean;
    onRun: () => void;
    onPause: () => void;
    onReset: () => void;
    status: string;
}

export const VMControls: React.FC<VMControlsProps> = ({
    isRunning,
    onRun,
    onPause,
    onReset,
    status,
}) => {
    return (
        <div
            className="vm-controls"
            style={{
                padding: '5px', // compact padding
                borderBottom: '1px solid var(--border-color)',
                display: 'flex',
                alignItems: 'center',
                backgroundColor: 'var(--bg-secondary)',
            }}
        >
            {/* Status on the left */}
            <div style={{ fontWeight: 'bold' }}>
                Status: <span style={{
                    color: status === 'Running' ? '#22c55e' :
                        status === 'Halted' ? '#ef4444' : '#eab308'
                }}>{status}</span>
            </div>
            {/* Buttons on the right */}
            <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
                <button
                    onClick={isRunning ? onPause : onRun}
                    className={isRunning ? 'pause-btn' : 'run-btn'}
                    style={{
                        padding: '4px 12px',
                        backgroundColor: isRunning ? '#eab308' : '#22c55e',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                    }}
                >
                    {isRunning ? 'Pause' : 'Run'}
                </button>
                <button
                    onClick={onReset}
                    style={{
                        padding: '4px 12px',
                        backgroundColor: '#ef4444',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                    }}
                >
                    Reset
                </button>
            </div>
        </div>
    );
};
