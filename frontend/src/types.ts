export interface Token {
    access_token: string;
    token_type: string;
}

export interface LoginRequest{
    email: string;
    password: string;
}

export interface UserCreate{
    email: string;
    password: string;
}

export interface UserOut{
    id: number;
    email: string;
    created_at: string;
}

export interface NoteOut{
    id: number;
    user_id: number;
    title: string;
    body: string;
    created_at: string;
    updated_at: string;
}

export interface NoteCreate{
    title: string;
    body: string;
}

export interface NoteUpdate{
    title?: string;
    body?: string;
}

export interface NoteListOut{
    items: NoteOut[];
    next_cursor: string | null;
}

export interface SearchResultOut{
    id: number;
    title: string;
    rank: number;
    headline: string;
}

export interface TagCreate{
    name: string;
}

export interface TagOut{
    id: number;
    name: string;
}

export interface SearchListOut{
    items: SearchResultOut[];
    next_cursor: string | null;
}