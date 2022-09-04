import Breakdown from 'components/breakdown';
import Layout from 'components/layout';
import { TransactionList } from 'components/transaction-list';
import { ToastHandler } from 'components/toast-handler';

export default function Home() {
    return (
        <Layout>
            <ToastHandler />
            <TransactionList />
            <Breakdown />
        </Layout>
    );
}
