import React, { useState, useRef, useEffect } from 'react';
import './SplitPane.css';

interface SplitPaneProps {
    left: React.ReactNode;
    right: React.ReactNode;
    initialSplit?: number; // Percentage
}

export const SplitPane: React.FC<SplitPaneProps> = ({ left, right, initialSplit = 50 }) => {
    const [split, setSplit] = useState(initialSplit);
    const splitPaneRef = useRef<HTMLDivElement>(null);
    const isDragging = useRef(false);

    const handleMouseDown = () => {
        isDragging.current = true;
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    };

    const handleMouseUp = () => {
        isDragging.current = false;
        document.body.style.cursor = 'default';
        document.body.style.userSelect = 'auto';
    };

    const handleMouseMove = (e: MouseEvent) => {
        if (!isDragging.current || !splitPaneRef.current) return;

        const { left, width } = splitPaneRef.current.getBoundingClientRect();
        const newSplit = ((e.clientX - left) / width) * 100;

        if (newSplit > 10 && newSplit < 90) {
            setSplit(newSplit);
        }
    };

    useEffect(() => {
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, []);

    return (
        <div className="split-pane" ref={splitPaneRef}>
            <div className="pane left" style={{ width: `${split}%` }}>
                {left}
            </div>
            <div className="resizer" onMouseDown={handleMouseDown} />
            <div className="pane right" style={{ width: `${100 - split}%` }}>
                {right}
            </div>
        </div>
    );
};
