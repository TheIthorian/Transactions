export const idMaker = (function* () {
    var index = -1;
    while (true) yield index--;
})();
