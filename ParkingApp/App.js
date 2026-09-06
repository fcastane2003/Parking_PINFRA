import { useState } from 'react';
import AppNavigator from './src/navigation/AppNavigator';

export default function App() {
  const [token, setToken] = useState(null);

  return <AppNavigator token={token} setToken={setToken} />;
}
