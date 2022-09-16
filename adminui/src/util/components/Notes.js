import React, { useEffect, useCallback, useState } from "react";
import Desc from "./Desc";
import { giveTransformDesc } from "../helper-functions/util-functions";

const Notes = ({ notes, cbref, cb, title, col, maxheight }) => {
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
    <div
      className={col || "col-md-4  "}
      
    >
      <h6 className="m-0 p-0">{title || "Admin Notes"}</h6>
      <div style={{ maxHeight: maxheight || "300px", overflowY: "auto", overflowX: "hidden" }} className="p-0 m-0">
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
      </div>
      <Desc
        cb={getData}
        col="col-12"
        placeholder="Add a note..."
        maxheight={maxheight}
      />
    </div>
  );
};

export default Notes;
