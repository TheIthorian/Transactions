import { Button } from 'antd';
import { useRouter } from 'next/router';
import { makeStore } from 'util/store';

export function Logout() {
    const router = useRouter();
    const handleClick = () => {
        makeStore('user').clear();
        router.push('/login');
    };

    return <Button onClick={handleClick}>Logout</Button>;
}
