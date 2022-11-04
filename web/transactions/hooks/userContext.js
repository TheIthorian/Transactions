import { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';

import { API_URL, API_KEY } from 'config';
import { makeStore } from 'util/store';

export const CurrentUserContext = createContext();

export const CurrentUserProvider = ({ children }) => {
    const store = makeStore('user');
    const [currentUser, setCurrentUser] = useState({});
    const [password, setPassword] = useState(store.get('password'));
    const [isLoggedIn, setIsLoggedIn] = useState(!!store.get('password'));
    const router = useRouter();

    useEffect(() => {
        if (!store.get('password')) {
            router.push('/login');
        }
    }, []);

    const fetchCurrentUser = async () => {
        let response = await fetch(API_URL, '/users/current', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Api-Key': API_KEY,
            },
        });
        response = await response.json();
        setCurrentUser({ ...response, password: store.get('password') });
    };

    return (
        <CurrentUserContext.Provider
            value={{ currentUser, isLoggedIn, fetchCurrentUser, password }}
        >
            {children}
        </CurrentUserContext.Provider>
    );
};

export const useCurrentUser = () => useContext(CurrentUserContext);
