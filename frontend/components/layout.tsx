import Head from 'next/head';
import styles from './layout.module.css';

export default function Layout(
  { children, input, hoho }: any
  ) {

    return (
      <div className={styles.container}>

        <header className={styles.header}>
          <div className={styles.connect_botton}>
            <w3m-button />
          </div>
          <div className={styles.inputBoxDiv}> {input} </div>

          <img style={{ 
                  position: "absolute", 
                  left: '7px',
                  top: `${hoho + 17}px`,
                  height: '34px',
                  width: '80px'
              }} 
              src="nouns-dao.png"/>

          <p className={styles.title}>Rep-Oracle</p>
        </header>

        <main className={styles.body}>
            {children}
        </main>

      </div>
    );  
}

