# Alt-Text Backend

## ROUTES

### /books

#### GET

##### FUNCTION

Gets a list of books from database

##### PARAMS

- query (string) | ensures book titles must have ‘query’ as a substring
- skip (int) | skips ‘skip’ amount of books from the result
- limit (int) | limits the amount of books returned to ‘limit’

##### RETURNS

```
[
  {
    title: string,
    description: string,
    cover: string,
  },
  ...
]
```

#### POST

##### FUNCTION

Adds a book to the database and starts initial processing

##### FIELDS

- title (string) | desired title for new book
- description (string) | desired description for new book
- cover (image_file) | desired cover image for new book
- file (file[.zip]) | book file (html and images bundled)

##### RETURNS

```
{
    title: string,
    description: string,
    cover: string,
}
```

### /books/:bookid

#### GET

#### PATCH

#### DELETE

### /books/:bookid/images

#### GET

#### PATCH

### /books/:bookid/images/:imagesrc

#### GET

#### PATCH
