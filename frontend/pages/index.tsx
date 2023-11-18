import Image from 'next/image'
import { useEffect, useRef, useState } from 'react';
import dynamic from "next/dynamic";
import styles from './index.module.css';
import Layout from '@/components/layout';


export default function Home() {

    useEffect(() => {
        // prevent scrolling
        document.body.style.overflow = "hidden";
        console.log('index useEffect  ');
    }, []);
  


  return (
    <Layout>
    </Layout>
  )
}
