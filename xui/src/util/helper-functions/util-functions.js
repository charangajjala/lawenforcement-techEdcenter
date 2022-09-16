export const giveBuffer = (inputObj) => {
  const bufferArrays = [];
  const addBuffer = (inputObj) => {
    for (const k in inputObj) {
      const val = inputObj[k];
      if (typeof val === "string") {
        bufferArrays.push({ e: true, message: `${k} : ${val}` });
      } else if (!Array.isArray(val)) {
        addBuffer(val);
      } else {
        for (const v of val) {
          if (typeof v === "string") {
            bufferArrays.push({ e: true, message: `${k} : ${v}` });
          } else {
            addBuffer(v);
          }
        }
      }
    }
  };
  addBuffer(inputObj);
  return bufferArrays;
};
export const giveTransformDesc = (descObj) => {
  const dumObj = { ...descObj };
  delete dumObj["lkey"];
  const descFinal = Object.values(dumObj);
  if (descFinal[descFinal.length - 1] === "") {
    descFinal.splice(-1);
  }
  return descFinal;
};

export const adjust = (entities, mode) => {
  return mode === "ADD"
    ? entities
        .filter((entity) => entity.action === "ADD")
        .map((entity) => {
          return { id: parseInt(entity.id), action: entity.action };
        })
    : entities
        .filter(
          (entity) =>
            (entity.old & (entity.action === "DELETE")) |
            (!entity.old & (entity.action === "ADD"))
        )
        .map((entity) => {
          return { id: parseInt(entity.id), action: entity.action };
        });
};
export const comapareArrays = (arr1, arr2) => {
  if (arr1.length !== arr2.length) return false;
  let same = true;
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) {
      same = false;
      break;
    }
  }
  return same;
};

export const getData = (ref, data) => {
  ref.current = data;
};

export const checkAddEmpty = (newObj) => {
  for (const key in newObj) {
    const newval = newObj[key];
    if (
      newval === undefined ||
      newval === null ||
      (Array.isArray(newval) && newval.length === 0) ||
      Number.isNaN(newval) ||
      newval === ""
    ) {
      delete newObj[key];
    }
  }
};

export const checkIfEdited = (newObj, compObj) => {
  for (const key in newObj) {
    const newval = newObj[key];
    if (
      Array.isArray(newval) &&
      (newval.length === 0 || comapareArrays(newval, compObj[key]))
    ) {
      delete newObj[key];
    } else if (typeof newval === "object" && newval !== null) {
      for (const k in newval) {
        if (newval[k] === compObj[key][k]) {
          delete newObj[key][k];
        }
      }
      if (Object.keys(newval).length === 0) delete newObj[key];
    } else if (newval === compObj[key]) {
      console.log(newval, compObj[key]);
      delete newObj[key];
    }
  }
};
export const validateAddress = (address, setAlertMessage, setShowAlert) => {
  const addres = address;

  if (
    address !== null &&
    (!addres.address1 ||
      !addres.address2 ||
      !addres.city ||
      !addres.state ||
      !addres.zip)
  ) {
    setAlertMessage({
      e: true,
      message:
        "One or more of address1, city, state, zip fields in Address is/are missing",
    });
    setShowAlert(true);
    return;
  }
};

export const validateContact = (contact, setAlertMessage, setShowAlert) => {
  if (contact !== null && (!contact.name || !contact.email || !contact.phone)) {
    setAlertMessage({
      e: true,
      message:
        "One or more of name, email, phone fields in  Contact is/are missing",
    });
    setShowAlert(true);
    throw new Error("address validation error");
  }
};

export const giveProperDate = (startDate, endDate) => {
  const start = new Date(startDate);
  const end = new Date(endDate);
  const options = { year: "numeric", month: "short", day: "numeric" };
  if (!endDate) {
    return `${start.toLocaleDateString("en-US", options)}`;
  }
  return `${start.toLocaleDateString(
    "en-US",
    options
  )} to ${end.toLocaleDateString("en-US", options)}`;
};
