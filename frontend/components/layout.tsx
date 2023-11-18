import Head from 'next/head';
import styles from './layout.module.css';

export const siteTitle = 'Omnitrace';


export default function Layout(
  { children }: any
  ) {

    return (
      <div className={styles.container}>
        <Head>
          <link rel="icon" href="/magnifier.png" />
          <meta
            name="description"
            content="Omnitrace"
          />
          <meta name="og:title" content={siteTitle} />
        </Head>

        <header className={styles.header}>
            <w3m-button />
          {/* <div className={GRAPHVIEW_TOP_BOX_STYLE}> 
            <div className={styles.inputBoxDiv}> {input} </div>
          </div>
          <div className={TABLEVIEW_TAB_BUTTON_GROUP_STYLE}> {topRightUI} </div>
          <div className={styles.bottomRightUI}> {bottomRightUI} </div>
          <div className={styles.bottomLeftUI}> {bottomLeftUI} </div> */}
        </header>

        <main className={styles.body}>{children}</main>

        {/* <footer className={styles.footer}>
          <div className={styles.bottomBox}> 
            {bottomLeftBox}
            <div className={styles.timeView}>{timeView}</div>   
            {bottomRightBox}
          </div>
        </footer> */}
      </div>
    );  
}

// className={styles.timeView}





// import { Inter } from 'next/font/google'

// const inter = Inter({ subsets: ['latin'] })

// export default function RootLayout({
//   children,
// }: {
//   children: React.ReactNode
// }) {
//   return (
//     <html lang="en">
//       <body className={inter.className}>{children}</body>
//     </html>
//   )
// }

