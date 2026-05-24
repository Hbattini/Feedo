import { ApolloProvider } from "./providers/ApolloProvider";
import { AuthProvider } from "./providers/AuthProvider";
import { AppRouter } from "../routes/AppRouter";

export function App() {
  return (
    <ApolloProvider>
      <AuthProvider>
        <AppRouter />
      </AuthProvider>
    </ApolloProvider>
  );
}
