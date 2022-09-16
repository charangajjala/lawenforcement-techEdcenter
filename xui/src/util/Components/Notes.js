import React, { useEffect, useCallback, useState } from "react";
import Desc from "./Desc";
import { giveTransformDesc } from "../helper-functions/util-functions";

const Notes = ({ notes, cbref, cb }) => {
  const [noteTexts, setNoteTexts] = useState([]);

  const getData = useCallback((notesObj) => {
    setNoteTexts(giveTransformDesc(notesObj));
  }, []);

  useEffect(() => {
    if (noteTexts) {
      cb(cbref, noteTexts);
    }
  }, [cb, cbref, noteTexts]);

  return (
    <div>
      <h5>Admin Notes</h5>
      {notes && (
        <ol className="list-group list-group-numbered">
          {notes.map((note) => (
            <li
              key={note.id}
              className="list-group-item d-flex justify-content-between align-items-start"
            >
              <div className="ms-2 me-auto text-dark">
                <div className="fw-bold">
                  {` By : ${note.createdBy.firstName} ${note.createdBy.lastName}    createdAt: ${note.created}`}
                </div>
                {note.text}
              </div>
            </li>
          ))}
        </ol>
      )}
      <Desc  cb={getData} placeholder="Add a note..." />
    </div>
  );
};

export default Notes;
