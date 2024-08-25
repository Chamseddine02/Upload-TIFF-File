// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [files, setFiles] = useState([]);
  const chunkSize = 5 * 1024 * 1024;

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadSuccess(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Aucun fichier sélectionné');
      return;
    }

    setIsLoading(true);
    const totalChunks = Math.ceil(file.size / chunkSize);
    const uploadId = Date.now().toString();

    // Upload chunks
    for (let i = 0; i < totalChunks; i++) {
      const formData = new FormData();
      formData.append('upload_id', uploadId);
      formData.append('chunk_index', i);
      formData.append('total_chunks', totalChunks);
      formData.append('file_name', file.name);
      formData.append('file_size', file.size);
      formData.append('file', file.slice(i * chunkSize, (i + 1) * chunkSize));

      await fetch('http://localhost:8000/upload_chunk/', {
        method: 'POST',
        body: formData,
      });
    }

    await fetch('http://localhost:8000/combine_chunks/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ upload_id: uploadId }),
    });

    setIsLoading(false);
    setUploadSuccess(true);
    fetchFiles();
  };

  const fetchFiles = () => {
    fetch('http://localhost:8000/files/')
      .then((response) => response.json())
      .then((data) => setFiles(data))
      .catch((error) => {
        console.error('Erreur lors de la récupération des fichiers:', error);
        alert('Erreur lors de la récupération des fichiers.');
      });
  };

  const handleDelete = (fileId) => {
    fetch(`http://localhost:8000/delete_file/${fileId}/`, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then(() => fetchFiles())
      .catch((error) => {
        console.error('Erreur lors de la suppression du fichier:', error);
        alert('Erreur lors de la suppression du fichier.');
      });
  };

  useEffect(() => {
    fetchFiles(); // Fetch files when the component mounts
  }, []);

  return (
    <div className="app">
      <h1>Upload un fichier</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          onChange={handleFileChange}
          style={{ cursor: 'pointer', marginBottom: '10px' }}
        />
        <button
          type="submit"
          disabled={isLoading}
          style={{ cursor: isLoading ? 'not-allowed' : 'pointer' }}
        >
          {isLoading ? 'IMPORTATION...' : 'IMPORTER'}
        </button>
        {isLoading && (
          <div className="loading">
            <img src="https://i0.wp.com/watan.org.tr/wp-content/uploads/2021/05/loading-gif-png-5.gif?quality=90&strip=all&ssl=1" alt="Chargement..." />
          </div>
        )}
      </form>
      {uploadSuccess && <p>Fichier importé avec succès</p>}
      <div className="file-list">
        <h2>Fichiers Téléchargés</h2>
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Taille</th>
              <th>Date de téléchargement</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.id}>
                <td>{file.name}</td>
                <td>{file.size} bytes</td>
                <td>{new Date(file.upload_date).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleDelete(file.id)}>Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
