<?php
/**
 * law_firm CPT + prefecture/crime_type タクソノミー登録
 */

add_action( 'init', 'kbn_register_cpt' );
function kbn_register_cpt(): void {
    register_post_type( 'law_firm', [
        'labels'      => [
            'name'          => '法律事務所',
            'singular_name' => '法律事務所',
        ],
        'public'      => true,
        'has_archive' => true,
        'rewrite'     => [ 'slug' => 'jimusho' ],
        'supports'    => [ 'title', 'thumbnail', 'custom-fields' ],
        'show_in_rest' => true,
    ] );
}

add_action( 'init', 'kbn_register_taxonomies' );
function kbn_register_taxonomies(): void {
    register_taxonomy( 'prefecture', 'law_firm', [
        'labels'       => [ 'name' => '都道府県' ],
        'public'       => true,
        'hierarchical' => false,
        'rewrite'      => [ 'slug' => 'ken' ],
        'show_in_rest' => true,
    ] );

    register_taxonomy( 'crime_type', 'law_firm', [
        'labels'       => [ 'name' => '罪種' ],
        'public'       => true,
        'hierarchical' => false,
        'rewrite'      => [ 'slug' => 'zaishu' ],
        'show_in_rest' => true,
    ] );
}
