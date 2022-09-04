/**
 * A class to interact with local storage
 * @roperty { string } storeId - Unique id of the store
 */
class Store {
    storeId;

    constructor(storeId = 'DefaultStore') {
        if (storeId) this.storeId = storeId;
    }

    /**
     * Returns all stored properties
     * @returns { Object }
     */
    getAll() {
        return JSON.parse(localStorage.getItem(this.storeId));
    }

    /**
     * Returns the value for a gievn property
     * @param   { string } property - Property name
     * @returns { any } - Property value
     */
    get(property) {
        const store = this.getAll() || {};
        return store[property];
    }

    /**
     * Stores a value against a given property
     * @param { string } property - Property name
     * @param { any } value - Value to store
     */
    set(property, value) {
        const store = this.getAll() || {};
        store[property] = value;
        localStorage.setItem(this.storeId, JSON.stringify(store));
    }

    /**
     * Replaces the entire store with a given object
     * @param { object } obj
     */
    replace(obj) {
        if (typeof obj === 'object') {
            localStorage.setItem(this.storeId, JSON.stringify(obj));
        }
    }

    /**
     * Clears the store
     */
    clear() {
        localStorage.removeItem(this.storeId);
    }

    /**
     * Clears all stores
     */
    clearAll() {
        localStorage.clear();
    }
}

class FakeStore {
    constructor() {}
    getAll() {}
    get() {}
    set() {}
    replace() {}
    clear() {}
    clearAll() {}
}

function makeStore() {
    if (typeof window !== 'undefined') {
        return new Store(...arguments);
    } else {
        return new FakeStore(...arguments);
    }
}

export { makeStore };
