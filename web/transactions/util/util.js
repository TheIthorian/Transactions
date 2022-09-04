export function uvl(value, _default) {
    return value === undefined ? _default : value;
}

export const idMaker = (function* () {
    var index = -1;
    while (true) yield index--;
})();
