<?php
/*
 * Template Name: 都道府県×罪種
 */

get_header();

$post_id     = get_the_ID();
$h1_heading  = get_post_meta( $post_id, 'h1_heading', true ) ?: get_the_title();
$bar_contact = get_post_meta( $post_id, 'local_bar_contact', true );
$court_name  = get_post_meta( $post_id, 'local_court_name', true );
$pref_slug   = get_post_meta( $post_id, 'prefecture_ref', true );
$crime_slug  = get_post_meta( $post_id, 'crime_type_ref', true );

$firms = new WP_Query( [
    'post_type'      => 'law_firm',
    'post_status'    => 'publish',
    'posts_per_page' => -1,
    'tax_query'      => [
        'relation' => 'AND',
        [
            'taxonomy' => 'prefecture',
            'field'    => 'slug',
            'terms'    => $pref_slug,
        ],
        [
            'taxonomy' => 'crime_type',
            'field'    => 'slug',
            'terms'    => $crime_slug,
        ],
    ],
] );
?>
<div class="kbn-page" style="max-width:900px;margin:0 auto;padding:20px 16px;">

  <h1 style="font-size:1.6em;margin-bottom:16px;"><?php echo esc_html( $h1_heading ); ?></h1>

  <?php if ( $bar_contact || $court_name ) : ?>
  <div style="background:#f7f7f7;border-left:4px solid #3182ce;padding:12px 16px;margin-bottom:24px;font-size:0.9em;">
    <?php if ( $bar_contact ) : ?>
      <p style="margin:4px 0;"><strong>当番弁護士:</strong> <?php echo esc_html( $bar_contact ); ?></p>
    <?php endif; ?>
    <?php if ( $court_name ) : ?>
      <p style="margin:4px 0;"><strong>管轄裁判所:</strong> <?php echo esc_html( $court_name ); ?></p>
    <?php endif; ?>
  </div>
  <?php endif; ?>

  <div id="search" style="margin-bottom:24px;"></div>

  <div class="kbn-firm-list">
    <?php if ( $firms->have_posts() ) : while ( $firms->have_posts() ) : $firms->the_post(); ?>
      <?php
        $fid          = get_the_ID();
        $is_24h_raw   = get_post_meta( $fid, 'is_24h', true );
        $hiyou_raw    = get_post_meta( $fid, 'hiyou_tokuya', true );
        $is_24h_str   = ( $is_24h_raw && $is_24h_raw !== '0' ) ? 'true' : 'false';
        $hiyou_str    = ( $hiyou_raw && $hiyou_raw !== '0' ) ? 'true' : 'false';
        $profile_text = get_post_meta( $fid, 'profile_text', true );
        $chakushukin  = (int) get_post_meta( $fid, 'chakushukin_min', true );
        $phone        = get_post_meta( $fid, 'phone_24h', true );
        $free_consult = get_post_meta( $fid, 'free_consultation', true );
        $filter_str   = "prefecture:{$pref_slug}, crime_type:{$crime_slug}, is_24h:{$is_24h_str}, hiyou_tokuya:{$hiyou_str}";
      ?>
      <div class="kbn-firm-card"
        data-pagefind-body
        data-pagefind-filter="<?php echo esc_attr( $filter_str ); ?>"
        style="border:1px solid #e2e8f0;border-radius:8px;padding:20px;margin-bottom:16px;">

        <h3 style="margin-top:0;margin-bottom:8px;"><?php the_title(); ?></h3>

        <p style="margin:0 0 10px;">
          <?php if ( $is_24h_str === 'true' ) : ?>
            <span style="background:#e53e3e;color:#fff;padding:2px 8px;border-radius:3px;font-size:12px;margin-right:4px;">24h対応</span>
          <?php endif; ?>
          <?php if ( $free_consult && $free_consult !== '0' ) : ?>
            <span style="background:#38a169;color:#fff;padding:2px 8px;border-radius:3px;font-size:12px;">無料相談</span>
          <?php endif; ?>
        </p>

        <?php if ( $profile_text ) : ?>
          <p style="color:#4a5568;margin-bottom:12px;"><?php echo esc_html( $profile_text ); ?></p>
        <?php endif; ?>

        <?php if ( $chakushukin > 0 ) : ?>
          <p style="margin-bottom:12px;"><strong>着手金:</strong> <?php echo number_format( $chakushukin ); ?>円〜</p>
        <?php endif; ?>

        <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
          <?php if ( $phone ) : ?>
            <a href="tel:<?php echo esc_attr( $phone ); ?>"
               style="background:#3182ce;color:#fff;padding:10px 20px;border-radius:4px;text-decoration:none;font-weight:bold;">
              <?php echo esc_html( $phone ); ?> に電話する
            </a>
          <?php endif; ?>
          <a href="<?php the_permalink(); ?>" style="color:#3182ce;">詳細を見る →</a>
        </div>

      </div>
    <?php endwhile; wp_reset_postdata();
    else : ?>
      <p style="color:#718096;">現在、この条件に一致する事務所情報はありません。</p>
    <?php endif; ?>
  </div>

</div>
<?php get_footer(); ?>
