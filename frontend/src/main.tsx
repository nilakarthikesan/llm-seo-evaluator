console.log('=== MAIN.TSX LOADING ===');
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

console.log('=== MAIN.TSX IMPORTS COMPLETE ===');
try {
  console.log('=== CREATING ROOT ===');
  createRoot(document.getElementById("root")!).render(<App />);
  console.log('=== ROOT CREATED SUCCESSFULLY ===');
} catch (error) {
  console.error('=== ROOT CREATION FAILED ===', error);
}
