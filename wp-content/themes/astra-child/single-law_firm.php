<?php get_header(); ?>

<?php while ( have_posts() ) : the_post(); ?>
  <?php
    $post_id      = get_the_ID();
    $phone        = get_post_meta( $post_id, 'phone_24h', true );
    $is_24h_raw   = get_post_meta( $post_id, 'is_24h', true );
    $profile_text = get_post_meta( $post_id, 'profile_text', true );
    $chakushukin  = (int) get_post_meta( $post_id, 'chakushukin_min', true );
    $address      = get_post_meta( $post_id, 'access_address', true );
    $website      = get_post_meta( $post_id, 'website_url', true );
    $free_consult = get_post_meta( $post_id, 'free_consultation', true );
    $hiyou_raw    = get_post_meta( $post_id, 'hiyou_tokuya', true );
    $is_24h       = $is_24h_raw && $is_24h_raw !== '0';
    $free         = $free_consult && $free_consult !== '0';
    $hiyou        = $hiyou_raw && $hiyou_raw !== '0';
  ?>
  <div style="max-width:800px;margin:0 auto;padding:20px 16px;">

    <h1 style="font-size:1.6em;margin-bottom:12px;"><?php the_title(); ?></h1>

    <p>
      <?php if ( $is_24h ) : ?>
        <span style="background:#e53e3e;color:#fff;padding:2px 8px;border-radius:3px;font-size:12px;margin-right:4px;">24h対応</span>
      <?php endif; ?>
      <?php if ( $free ) : ?>
        <span style="background:#38a169;color:#fff;padding:2px 8px;border-radius:3px;font-size:12px;margin-right:4px;">無料相談</span>
      <?php endif; ?>
      <?php if ( $hiyou ) : ?>
        <span style="background:#805ad5;color:#fff;padding:2px 8px;border-radius:3px;font-size:12px;">費用特約対応</span>
      <?php endif; ?>
    </p>

    <?php if ( $profile_text ) : ?>
      <p style="color:#4a5568;line-height:1.7;"><?php echo esc_html( $profile_text ); ?></p>
    <?php endif; ?>

    <?php if ( $chakushukin > 0 ) : ?>
      <p><strong>着手金:</strong> <?php echo number_format( $chakushukin ); ?>円〜</p>
    <?php endif; ?>

    <?php if ( $address ) : ?>
      <p><strong>住所:</strong> <?php echo esc_html( $address ); ?></p>
    <?php endif; ?>

    <?php if ( $phone ) : ?>
      <div style="margin:24px 0;">
        <a href="tel:<?php echo esc_attr( $phone ); ?>"
           style="background:#e53e3e;color:#fff;padding:14px 28px;border-radius:6px;text-decoration:none;font-size:1.1em;font-weight:bold;display:inline-block;">
          今すぐ電話: <?php echo esc_html( $phone ); ?>
        </a>
      </div>
    <?php endif; ?>

    <?php if ( $website ) : ?>
      <p><a href="<?php echo esc_url( $website ); ?>" target="_blank" rel="noopener noreferrer"
            style="color:#3182ce;">公式サイトを見る →</a></p>
    <?php endif; ?>

  </div>
<?php endwhile; ?>

<?php get_footer(); ?>
