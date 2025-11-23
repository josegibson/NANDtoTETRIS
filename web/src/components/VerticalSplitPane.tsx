import React, { useState, useRef, useEffect } from 'react';
import './VerticalSplitPane.css';

interface VerticalSplitPaneProps {
    top: React.ReactNode;
    bottom: React.ReactNode;
    initialSplit?: number; // Percentage
}

export const VerticalSplitPane: React.FC<VerticalSplitPaneProps> = ({ top, bottom, initialSplit = 60 }) => {
    const [split, setSplit] = useState(initialSplit);
    const splitPaneRef = useRef<HTMLDivElement>(null);
    const isDragging = useRef(false);

    const handleMouseDown = () => {
        isDragging.current = true;
        document.body.style.cursor = 'row-resize';
        document.body.style.userSelect = 'none';
    };

    const handleMouseUp = () => {
        isDragging.current = false;
        document.body.style.cursor = 'default';
        document.body.style.userSelect = 'auto';
    };

    const handleMouseMove = (e: MouseEvent) => {
        if (!isDragging.current || !splitPaneRef.current) return;

        const { top, height } = splitPaneRef.current.getBoundingClientRect();
        const newSplit = ((e.clientY - top) / height) * 100;

        if (newSplit > 20 && newSplit < 80) {
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
        <div className="vertical-split-pane" ref={splitPaneRef}>
            <div className="pane top" style={{ height: `${split}%` }}>
                {top}
            </div>
            <div className="resizer horizontal" onMouseDown={handleMouseDown} />
            <div className="pane bottom" style={{ height: `${100 - split}%` }}>
                {bottom}
            </div>
        </div>
    );
};
