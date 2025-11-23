import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Vm, ParsedVmFile } from '../simulator/vm/vm';
import { VM } from '../simulator/languages/vm';
import { Screen, reduceScreen } from './Screen';
import { VMControls } from './VMControls';
import { isErr, unwrap, ErrResult } from '../simulator/util/result';
import { KEYBOARD_OFFSET } from '../simulator/cpu/memory';

interface VMEmulatorProps {
    vmFiles: { name: string; content: string }[];
}

export const VMEmulator: React.FC<VMEmulatorProps> = ({ vmFiles }) => {
    const [vm, setVm] = useState<Vm | null>(null);
    const [isRunning, setIsRunning] = useState(false);
    const [status, setStatus] = useState('Ready');
    const speed = 100; // Maximum speed
    const [error, setError] = useState<string | null>(null);
    const requestRef = useRef<number>();



    // Initialize VM
    useEffect(() => {
        // Reset state when vmFiles is empty or undefined
        if (!vmFiles || vmFiles.length === 0) {
            setVm(null);
            setError(null);
            setStatus('No VM files available');
            return;
        }

        try {
            // Reset error state at the start of initialization
            setError(null);
            setStatus('Initializing...');

            const parsedFiles: ParsedVmFile[] = [];

            for (const file of vmFiles) {
                const match = VM.parse(file.content);
                if (isErr(match)) {
                    const errorMsg = `Parse error in ${file.name}: ${(match as ErrResult<Error>).error.message}`;
                    setError(errorMsg);
                    setVm(null); // Ensure vm is null on error
                    return;
                }
                parsedFiles.push({
                    name: file.name,
                    instructions: unwrap(match).instructions
                });
            }

            const result = Vm.buildFromFiles(parsedFiles);
            if (isErr(result)) {
                const errorMsg = `VM Build error: ${(result as ErrResult<Error>).error.message}`;
                setError(errorMsg);
                setVm(null); // Ensure vm is null on error
                return;
            }

            setVm(unwrap(result));
            setStatus('Ready');
            setError(null);
        } catch (e) {
            const errorMsg = `Unexpected error: ${e instanceof Error ? e.message : String(e)}`;
            setError(errorMsg);
            setVm(null); // Ensure vm is null on error
        }
    }, [vmFiles]);

    const isRunningRef = useRef(isRunning);

    // Keep ref in sync with state
    useEffect(() => {
        isRunningRef.current = isRunning;
    }, [isRunning]);

    // Execution Loop
    const animate = useCallback((_time: number) => {
        if (!vm || !isRunningRef.current) return;

        try {
            // Execute multiple steps per frame based on speed
            const stepsPerFrame = Math.floor(speed * 10);

            for (let i = 0; i < stepsPerFrame; i++) {
                const exitCode = vm.step();
                if (exitCode !== undefined) {
                    setIsRunning(false);
                    setStatus(`Halted (Exit Code: ${exitCode})`);
                    return;
                }
            }

            requestRef.current = requestAnimationFrame(animate);
        } catch (e) {
            setIsRunning(false);
            setStatus('Error');
            setError(`Runtime error: ${e instanceof Error ? e.message : String(e)}`);
        }
    }, [speed, vm]);

    useEffect(() => {
        if (isRunning) {
            requestRef.current = requestAnimationFrame(animate);
        } else {
            if (requestRef.current) {
                cancelAnimationFrame(requestRef.current);
            }
        }
        return () => {
            if (requestRef.current) {
                cancelAnimationFrame(requestRef.current);
            }
        };
    }, [isRunning, animate]);

    // Keyboard Handling
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (!vm) return;

            let key = 0;
            if (e.key.length === 1) {
                key = e.key.charCodeAt(0);
            } else {
                switch (e.key) {
                    case 'Enter': key = 128; break;
                    case 'Backspace': key = 129; break;
                    case 'ArrowLeft': key = 130; break;
                    case 'ArrowUp': key = 131; break;
                    case 'ArrowRight': key = 132; break;
                    case 'ArrowDown': key = 133; break;
                    case 'Home': key = 134; break;
                    case 'End': key = 135; break;
                    case 'PageUp': key = 136; break;
                    case 'PageDown': key = 137; break;
                    case 'Insert': key = 138; break;
                    case 'Delete': key = 139; break;
                    case 'Escape': key = 140; break;
                    case 'F1': key = 141; break;
                    case 'F2': key = 142; break;
                    case 'F3': key = 143; break;
                    case 'F4': key = 144; break;
                    case 'F5': key = 145; break;
                    case 'F6': key = 146; break;
                    case 'F7': key = 147; break;
                    case 'F8': key = 148; break;
                    case 'F9': key = 149; break;
                    case 'F10': key = 150; break;
                    case 'F11': key = 151; break;
                    case 'F12': key = 152; break;
                }
            }

            if (key > 0) {
                vm.memory.set(KEYBOARD_OFFSET, key);
            }
        };

        const handleKeyUp = () => {
            if (!vm) return;
            vm.memory.set(KEYBOARD_OFFSET, 0);
        };

        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
        };
    }, [vm]);

    const handleReset = () => {
        if (vm) {
            setIsRunning(false);
            vm.reset();
            setStatus('Ready');
        }
    };

    if (error) {
        return (
            <div className="vm-error" style={{ color: 'red', padding: '20px' }}>
                <h3>VM Error</h3>
                <pre>{error}</pre>
            </div>
        );
    }

    if (!vm) {
        return (
            <div style={{ padding: '20px', color: error ? 'red' : 'inherit' }}>
                {status}
            </div>
        );
    }

    return (
        <div className="vm-emulator" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <VMControls
                isRunning={isRunning}
                onRun={() => {
                    setIsRunning(true);
                    setStatus('Running');
                }}
                onPause={() => { setIsRunning(false); setStatus('Paused'); }}
                onReset={handleReset}
                status={status}
            />

            <div className="vm-screen-container" style={{
                flex: 1,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'flex-start',
                backgroundColor: '#1e1e1e',
                paddingTop: '5px'
            }}>
                <Screen memory={reduceScreen(vm.memory.screen)} scale={1} showScaleControls={false} />
            </div>
        </div>
    );
};
