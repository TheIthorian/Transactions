export function memoize(fn) {
    const cache = {};

    return function (...args) {
        if (cache[args]) {
            return cache[args];
        }

        cache[args] = fn(...args);
        return cache[args];
    };
}
