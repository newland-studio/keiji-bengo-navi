<?php
add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style( 'astra-child-style', get_stylesheet_uri() );
} );

require_once get_stylesheet_directory() . '/inc/cpt.php';

add_filter( 'acf/settings/load_json', function ( $paths ) {
    $paths[] = get_stylesheet_directory() . '/acf-json';
    return $paths;
} );
add_filter( 'acf/settings/save_json', function () {
    return get_stylesheet_directory() . '/acf-json';
} );

// Pagefind UI の読み込み
add_action( 'wp_footer', function () {
    if ( is_post_type_archive( 'law_firm' ) || is_page_template( 'page-ken-crime.php' ) ) :
    ?>
    <link href="/pagefind/pagefind-ui.css" rel="stylesheet">
    <script src="/pagefind/pagefind-ui.js"></script>
    <script>
    window.addEventListener('DOMContentLoaded', () => {
        new PagefindUI({
            element: '#search',
            showImages: false,
            filters: {
                prefecture:   { label: '都道府県' },
                crime_type:   { label: '罪種' },
                is_24h:       { label: '24時間対応' },
                hiyou_tokuya: { label: '費用特約対応' },
            }
        });
    });
    </script>
    <?php
    endif;
} );
