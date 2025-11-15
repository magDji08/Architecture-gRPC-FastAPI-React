import React, { useEffect, useState } from "react";
import { getUsers, createUser, updateUser, deleteUser } from "./services/api";
import ServiceMonitor from "./components/ServiceMonitor";
import "./App.css";

function App() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ first_name: "", last_name: "", age: "", email: "" });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getUsers();
      setUsers(res.data.users);
    } catch (err) {
      setError("Erreur lors du chargement des utilisateurs. Vérifiez que le serveur est démarré.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const showSuccess = (message) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(""), 3000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!form.first_name || !form.last_name || !form.age || !form.email) {
      setError("Tous les champs sont requis");
      return;
    }

    if (!/\S+@\S+\.\S+/.test(form.email)) {
      setError("Format d'email invalide");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      if (editingId) {
        await updateUser(editingId, { ...form, age: parseInt(form.age) });
        showSuccess("✅ Utilisateur modifié avec succès !");
        setEditingId(null);
      } else {
        await createUser({ ...form, age: parseInt(form.age) });
        showSuccess("✅ Utilisateur créé avec succès !");
      }

      setForm({ first_name: "", last_name: "", age: "", email: "" });
      await loadUsers();
    } catch (err) {
      setError("Erreur lors de l'opération. Vérifiez les données.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (user) => {
    setForm(user);
    setEditingId(user.id);
    setError(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancel = () => {
    setForm({ first_name: "", last_name: "", age: "", email: "" });
    setEditingId(null);
    setError(null);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?")) {
      try {
        setLoading(true);
        await deleteUser(id);
        showSuccess("✅ Utilisateur supprimé avec succès !");
        await loadUsers();
      } catch (err) {
        setError("Erreur lors de la suppression");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🚀 Gestion des Utilisateurs</h1>
        <p className="subtitle">Architecture: gRPC + FastAPI + React</p>
      </header>

      <main className="main-content">
        {error && (
          <div className="alert alert-error">
            ❌ {error}
            <button onClick={() => setError(null)} className="close-btn">×</button>
          </div>
        )}

        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
          </div>
        )}

        {/* Monitoring des Services */}
        <ServiceMonitor />

        <div className="form-card">
          <h2>{editingId ? "✏️ Modifier l'utilisateur" : "➕ Créer un utilisateur"}</h2>
          <form onSubmit={handleSubmit} className="user-form">
            <div className="form-row">
              <div className="form-group">
                <label>Prénom *</label>
                <input
                  type="text"
                  placeholder="Entrez le prénom"
                  value={form.first_name}
                  onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                  disabled={loading}
                  required
                />
              </div>
              <div className="form-group">
                <label>Nom *</label>
                <input
                  type="text"
                  placeholder="Entrez le nom"
                  value={form.last_name}
                  onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Âge *</label>
                <input
                  type="number"
                  placeholder="Entrez l'âge"
                  value={form.age}
                  onChange={(e) => setForm({ ...form, age: e.target.value })}
                  disabled={loading}
                  min="1"
                  max="120"
                  required
                />
              </div>
              <div className="form-group">
                <label>Email *</label>
                <input
                  type="email"
                  placeholder="exemple@email.com"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "⏳ Chargement..." : editingId ? "✏️ Mettre à jour" : "➕ Créer"}
              </button>
              {editingId && (
                <button type="button" onClick={handleCancel} className="btn btn-secondary" disabled={loading}>
                  ❌ Annuler
                </button>
              )}
            </div>
          </form>
        </div>

        <div className="table-card">
          <div className="table-header">
            <h2>📋 Liste des Utilisateurs</h2>
            <span className="user-count">{users.length} utilisateur(s)</span>
          </div>

          {loading && users.length === 0 ? (
            <div className="loading">⏳ Chargement des utilisateurs...</div>
          ) : users.length === 0 ? (
            <div className="empty-state">
              <p>📭 Aucun utilisateur trouvé</p>
              <p className="empty-subtitle">Créez votre premier utilisateur ci-dessus</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="users-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Prénom</th>
                    <th>Nom</th>
                    <th>Âge</th>
                    <th>Email</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u.id} className={editingId === u.id ? "editing" : ""}>
                      <td>#{u.id}</td>
                      <td>{u.first_name}</td>
                      <td>{u.last_name}</td>
                      <td>{u.age} ans</td>
                      <td>{u.email}</td>
                      <td>
                        <div className="action-buttons">
                          <button 
                            onClick={() => handleEdit(u)} 
                            className="btn btn-edit"
                            disabled={loading}
                            title="Modifier"
                          >
                            ✏️
                          </button>
                          <button 
                            onClick={() => handleDelete(u.id)} 
                            className="btn btn-delete"
                            disabled={loading}
                            title="Supprimer"
                          >
                            🗑️
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Projet ProtoBuf & gRPC - Web Avancé 2025</p>
      </footer>
    </div>
  );
}

export default App;
