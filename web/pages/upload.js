import Layout from 'components/layout';
import { ToastHandler } from 'components/toast-handler';
import { CurrentUserProvider } from 'hooks/userContext';
import { Logout } from 'components/logout';
import { TransactionUpload } from 'components/transaction-upload';

export default function BudgetPage() {
    return (
        <CurrentUserProvider>
            <Layout>
                <ToastHandler />
                <Logout />
                <TransactionUpload />
            </Layout>
        </CurrentUserProvider>
    );
}
