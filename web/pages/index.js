import Breakdown from 'components/breakdown';
import Layout from 'components/layout';
import { TransactionList } from 'components/transaction-list';
import { ToastHandler } from 'components/toast-handler';
import { TransactionTimeline } from 'components/transaction-timeline';
import { CurrentUserProvider } from 'hooks/userContext';
import { Logout } from 'components/logout';

export default function Home() {
    return (
        <CurrentUserProvider>
            <Layout>
                <ToastHandler />
                <Logout />
                <TransactionList />
                <Breakdown />
                <TransactionTimeline />
            </Layout>
        </CurrentUserProvider>
    );
}
