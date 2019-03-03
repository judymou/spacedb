export function parseQuery(queryString) {
  const query = {};
  if (!queryString) {
    return query;
  }
  const firstChar = queryString[0];
  const cleanedString = firstChar === '?' || firstChar === '#' ?
          queryString.substr(1) : queryString;
  const pairs = cleanedString.split('&');
  for (let i = 0; i < pairs.length; i++) {
    const pair = pairs[i].split('=');
    query[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
  }
  return query;
}
