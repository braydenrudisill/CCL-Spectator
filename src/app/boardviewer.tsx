'use client'
import React, { useState, useEffect, useRef } from 'react'
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";
import { Card, Grid, Paper, styled } from '@mui/material';

const BoardViewer = ({ size, username, port } : BoardProps) => {
    const [game, setGame] = useState(new Chess());
    const [moves, setMoves] = useState([[]])

    const pgnEndRef = useRef(null)

    async function getMoves() {
        try {
          const res = await fetch(`http://127.0.0.1:500`+port+`/get_live_data?username=`+username,{
            method: "GET",
            headers: {
              "access-control-allow-origin" : "*",
              "Content-type": "application/json; charset=UTF-8",
              'Cache-Control': 'no-cache'
            }});
      
          if (!res.ok) {
            throw new Error('Failed to fetch data');
          }
          
          res.json().then(m => {
            setMoves(m)
            game.loadPgn(m.flat().join(' '))
          })
        } catch (err) {
          console.log(err);
        }
    }
    const scrollToBottom = () => {
        pgnEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }
    
      useEffect(() => {
        scrollToBottom()
      }, [moves]);

    useEffect(()=>{
        const intervalID = setInterval(() =>  {
            getMoves()
        }, 500);
    
        return () => clearInterval(intervalID);
    }, [])

    const boardStyle: React.CSSProperties = {
        display: 'flex',
        flexDirection: 'row',
        maxHeight: size,
        maxWidth: size+100,
    }

    const pgnView = moves.flat().map((move, i: number) =>
        <Grid item xs={6} key={i}>
            {move}
        </Grid>
    );
    return (
        <Card style={boardStyle}>
            <Chessboard boardWidth={size} position={game.fen()} id="BasicBoard"/>
            <Grid container style={scrollable} justifyContent="center">
                {pgnView}
                <div ref={pgnEndRef} />
            </Grid>
        </Card>
    )
}

const scrollable: React.CSSProperties = {
    overflow: 'auto',
}

type BoardProps = {
    size: number;
    username: string;
    port: number;
};

export default BoardViewer