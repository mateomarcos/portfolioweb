function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  function deleteProject(projectId) {
    fetch("/delete-project", {
      method: "POST",
      body: JSON.stringify({ projectId : projectId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }