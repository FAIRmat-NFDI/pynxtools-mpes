import '@h5web/app/styles.css';

import { App } from '@h5web/app';
import { H5WasmLocalFileProvider } from '@h5web/h5wasm';
import { useState } from 'react';
import { createRoot } from 'react-dom/client';

function Viewer() {
  const [file, setFile] = useState<File>();

  if (!file) {
    return (
      <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
        <h1>H5Web</h1>
        <p>Pick an HDF5/NeXus file to explore. It's read locally in this browser tab - nothing is uploaded anywhere.</p>
        <input
          aria-label="Pick HDF5 file"
          type="file"
          accept=".h5,.hdf,.hdf5,.nx,.nxs,.nx5,.nexus"
          onChange={(evt) => setFile(evt.target.files?.[0])}
        />
      </div>
    );
  }

  return (
    <div style={{ height: '100vh' }}>
      <H5WasmLocalFileProvider file={file}>
        <App />
      </H5WasmLocalFileProvider>
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<Viewer />);
