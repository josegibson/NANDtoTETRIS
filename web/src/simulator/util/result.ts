export type Result<T, E = Error> = OkResult<T> | ErrResult<E>;

export class OkResult<T> {
    constructor(public value?: T) { }
}

export class ErrResult<E> {
    constructor(public error: E) { }
}

export const Ok = <T>(value?: T) => new OkResult(value);
export const Err = <E>(error: E) => new ErrResult(error);

export function isOk<T, E>(result: Result<T, E>): result is OkResult<T> {
    return result instanceof OkResult;
}

export function isErr<T, E>(result: Result<T, E>): result is ErrResult<E> {
    return result instanceof ErrResult;
}

export function unwrap<T, E>(result: Result<T, E>): T {
    if (isErr(result)) {
        throw result.error;
    }
    return result.value as T;
}
