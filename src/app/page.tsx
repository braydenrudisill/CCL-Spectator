import React, { Suspense } from 'react';
import BoardViewer from '@/app/boardviewer';
import { Card, List, Button } from '@mui/material';

export default async function Page() {

  return (
    <>
      <BoardViewer size={200} username='Hikaru' port={0}/>
      <BoardViewer size={200} username='Jumbo' port={0}/>
    </>
  )
}
