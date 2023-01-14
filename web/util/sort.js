export function dateSort(a, b) {
    if (!a || !b) {
        return a ? Infinity : -Infinity;
    }
    return b - a;
}

export function textSort(a, b) {
    if (!a || !b) {
        return a ? Infinity : -Infinity;
    }
    return ('' + b.toUpperCase()).localeCompare(a.toUpperCase());
}

export function textSortCaseSensitive(a, b) {
    if (!a || !b) {
        return a ? Infinity : -Infinity;
    }
    return ('' + b).localeCompare(a);
}
